"""
Module documentator - Generates documentation for a Rocketbot module.

This script assume that the package module has description field in all attributes.

    Usage:
        documentator.py [--module, -m] [--readme, -r] [--lang, -l] [--help, -h] <module>
        
    Options:
        -h --help     Show this screen.
        --version, -v     Show version.
        --all, -a         Generate all documentation, readme and manual.
        --module, -m      Generate documentation for a module.
        --readme, -r      Generate readme for a module.
        --lang, -l        Language of the documentation.

    Examples:
        documentator.py -a -m -l en /home/user/Rocketbot/modules/advancedExcel 
        documentator.py

    This file can also be imported as a module and contains the following
    classes:
        - Documentator: Generates documentation for a Rocketbot module.
        - Package:      Class that represent the package file of a module.
        - Module:       Class with funtion related with a module.
"""

__version__ = "0.1.0"
__author__ = "Danilo Toro"
__license__ = "MIT"


import json
import os
from mdutils.mdutils import MdUtils
import git
import re


LICENSES = {
    "MIT": {
        "url": "http://opensource.org/licenses/mit-license.ph",
        "image": "https://camo.githubusercontent.com/107590fac8cbd65071396bb4d04040f76cde5bde/687474703a2f2f696d672e736869656c64732e696f2f3a6c6963656e73652d6d69742d626c75652e7376673f7374796c653d666c61742d737175617265"
    }
}

LANGUAGE={
    "how_to_install":{"es": "Como instalar este ", "en": "Howto install this "},
    "how_to_use": {"es": "Como usar este ", "en": "How to use this "},
    "module": {"es": "módulo", "en": "module"},
    "options": {"es": "Opciones", "en": "Options"},
    "parameters": {"es": "Parámetros", "en": "Parameters"},
    "description": {"es": "Descripción", "en":"Description"},
    "example": {"es": "ejemplo", "en":"example"},
    "installation": {
        "es": lambda folder: f"__Descarga__ e __instala__ el contenido en la carpeta '{folder}s' en la ruta de rocketbot.",
        "en": lambda folder: f"__Download__ and __install__ the content in '{folder}s' folder in Rocketbot path"
    },
    "overview_module": {
        "es": "Descripción de los comandos", "en": "Description of the commands"
    },
    "overview_addon": {
        "es": "Configuración", "en": "Configuration"
    },
    "language": {
        "es": "Español",
        "en": "English"
    }
}

class Package:
    """
    Representation of the package file of a module.

    ...
    Attributes
    ----------
    all first level attributes on the package (name, version, author, etc)
    os : list
        list with the operative system suported

    Methods
    -------
    get_attribute(object, name, lang="en")
        Return the value of a property in a dict validating all type of combination

    get_component_type(lang="en")
        Return the type of component (module or addon)
    
    """

    def __init__(self, json_package: dict):
        """Initialize the package.

        Parameters.
        ----------
        json_package : dict
            dictionary with the package file read
        """
        self.__dict__.update(json_package)
        self.__os_supported()
        self.__create_dependencies()

    def __os_supported(self):
        self.os = []
        if self.windows:
            self.os.append("windows")
        if self.mac:
            self.os.append("mac")
        if self.linux:
            self.os.append("linux")
        if self.docker:
            self.os.append("docker")

    def __create_dependencies(self):
        for name in self.dependencies.keys():
            url = f"https://pypi.org/project/{name}/"
            self.dependencies[name] = url
        
    def get_attribute(self, object, name, lang="en")->str:
        """Return the attribute in a package object.

        Objects can be:
        - {"title":{"es": "}} 
        - {"es":{"title": "}}        
        
        Parameters
        ----------
        object : dict
            The object where get the attribute
        name : str
            Name of the attribute
        lang : str, optional
            Language of the attribute. The default is "en".

        Returns
        -------
        str
            The value of the attribute. If not found, return empty str.
        
        """
        if lang in object:
            return object[lang][name] if name in object[lang] else ""
        if name in object and isinstance(object[name], dict):
            if lang in object[name]:
                return object[name][lang]
            if "en" in object[name]:
                return object[name]["en"]
        if name in object:
            return object[name]
        return ""

    def get_component_type(self)->str:
        """Return the type of component (module or addon).

        Returns
        -------
        str
            The type of component.
        """
        component = "module"
        if hasattr(self, "type"):
            component = self.type
        return component

class Documentator:
    """
    A class to generate the documentation of a module.

    ...

    Attributes
    ----------
    path : str
        Path of the module.
    name : str
        Name of the module.
    package : Package
        Package of the module represented as object.

    Methods
    -------
    read_package()
        Read the package file and create the package object.
    to_readme(path_to_save="", lang="en", comment="")
        Generate the README.md file.
    to_manual(path_to_save="", lang="en", banner_path="")
        Generate the manual of the module as Manual_{name}.md file.
    
    """

    def __init__(self, module_path: str):
        """
        Initialize the documentator.

        Parameters
        ----------
        module_path : str
            Path of the module.
        """
        self.path = module_path
        self.name = self.path.split('/')[-1]
        self.module = Module(self.path)
        self.package = self.module.package

    def __create_md_base(self, path_to_save: str, lang:str, banner_path: str="")->MdUtils:
        component_type = self.package.get_component_type()
        md_file = MdUtils(file_name=path_to_save)
        md_file.new_header(level=1, title=self.package.title[lang])
        self.__add_description_module(md_file, self.package.description, lang)

        if banner_path:
            md_file.new_line(
                md_file.new_inline_image("banner", banner_path)
            )

        #How to install section
        md_file.new_header(level=2, title=LANGUAGE["how_to_install"][lang] + LANGUAGE[component_type][lang])
        md_file.new_line(LANGUAGE["installation"][lang](component_type))
        md_file.new_line("\n\n")
        #How to use section
        self.__add_how_to_use(md_file, lang)
        return md_file

    def __add_how_to_use(self, md_file: MdUtils, lang: str)->MdUtils:
        if not os.path.exists(f"{self.path}/docs/how_to_use.md"):
            return md_file

        with open(f"{self.path}/docs/how_to_use.md", "r", encoding="utf-8") as f:
            how_to_use = f.read()
        how_to_use = how_to_use.split("---")
        l = ["en", "es", "pr"]
        how_to_use = how_to_use[l.index(lang)]
        md_file.write(how_to_use)
            
    def to_readme(self, path_to_save="", lang="en")->None:
        """Generate the README.md file.

        Parameters
        ----------
        path_to_save : str, optional
            Path to save the README.md file. The default is in the module path.
        lang : str, optional
            Language of the README.md file. The default is "en".

        Returns
        -------
        None
        """
        if not path_to_save:
            path_to_save = os.path.join(self.path, "README.md")
        md_file = self.__create_md_base(path_to_save, lang)

        # Create description section
        md_file.new_header(level=2, title="Overview")
        for i, command in enumerate(self.package.children, start=1):
            title = self.package.get_attribute(command, "title", lang)
            description = self.package.get_attribute(command, "description", lang)
            md_file.new_paragraph(f"{i}. {title}")
            md_file.new_line(description)
        
        # Create updates section
        md_file.new_line("\n\n")
        self.__add_updates(md_file)
        md_file.new_paragraph("----")

        # Create Os section
        md_file.new_header(level=3, title="OS")
        md_file.new_list(self.package.os)

        #Create dependencies section
        md_file.new_header(level=3, title="Dependencies")
        self.__add_dependencies(md_file, self.package.dependencies)

        #Create license section
        md_file.new_header(level=3, title="License")
        self.__add_license(md_file, self.package.license)

        # Save the file
        md_file.create_md_file()

    def __add_updates(self, md: MdUtils)->None:
        changes_file = self.path + "/CHANGES.txt"
        if os.path.exists(changes_file):
            with open(changes_file, 'r') as f:
                md.new_header(level=3, title="Changes")
                md.write(f.read())
                    
    def __add_description_module(self, md: MdUtils, description: str, lang: str)->None:
        if "|" not in description:
            description = description + " | " + description

        desc_splitted = description.split("| ")
        l = ["es", "en", "pr"]
        description = desc_splitted[l.index(lang)]
        md.new_line(description.strip())
        md.new_line()

    def __add_command_image(self, md: MdUtils, module_name: str, img_folder:str)->MdUtils:
        image_path = os.path.join(img_folder,module_name +".png")
        if os.path.exists(os.path.join(self.path, image_path)):
            md.new_line(
                md.new_inline_image(module_name, image_path)
            )
        return md

    def __add_dependencies(self, md: MdUtils, dependencies: dict)->None:
        for dependencie in dependencies:
            md.write(
                "- " + md.new_inline_link(link=dependencies[dependencie], text=dependencie, bold_italics_code='b')
            )    

    def __add_license(self, md: MdUtils, license:str)->None:
        text = license
        path = LICENSES[license]["image"]
        url = LICENSES[license]["url"]
        md.new_line(md.new_inline_image(text,path))
        md.new_line(md.new_inline_link(url, text))

    def to_manual(self, path_to_save="", lang="es", banner_path=""):
        """Generate the Manual_module_name.md file.

        Parameters
        ----------
        path_to_save : str, optional
            Path to save the Manual_module_name.md file. The default is in the module path.
        lang : str, optional
            Language of the Manual_module_name.md file. The default is "es".
        banner_path : str, optional
            Path to the banner image. The default is in docs/imgs.
        """
        if not path_to_save:
            path_to_save = self.module.doc_path
        
        if not banner_path:
            banner_path = "/docs/imgs/Banner_{name}.png".format(name=self.name)

        md_file = self.__create_md_base(path_to_save, lang, banner_path)

        # Create description section
        md_file.new_header(level=2, title=LANGUAGE["overview_"+self.package.get_component_type()][lang])
        for command in self.package.children:
            title = self.package.get_attribute(command, "title", lang)
            description = self.package.get_attribute(command, "description", lang)
            md_file.new_header(level=3, title=title)
            md_file.new_line(description)
            table = [LANGUAGE["parameters"][lang], LANGUAGE["description"][lang], LANGUAGE["example"][lang]]
            for input in command["form"]["inputs"]:
                table.extend([
                    self.package.get_attribute(input, "title", lang).replace(":", ""),
                    self.package.get_attribute(input, "description", lang).replace(":", ""),
                    self.package.get_attribute(input, "placeholder", lang),
                ])
            md_file.new_table(columns=3, rows=len(table)//3, text=table, text_align=None)
            self.__add_command_image(md_file, command["module"], "example")

        # Save the file
        md_file.create_md_file()   
        
class Module:
    """Class to represent a module.

    Attributes
    ----------
    path : str
        Path to the module folder.
    package : Package
        Package object.
    docs_path : str
        Path to the docs folder.
    name : str
        Name of the module.

    Methods
    -------
    read_package()
        Read the package.json file and create the Package object.
    create_docs_path()
        Create the docs folder.
    create_logs()
        Create the logs file.

    """

    def __init__(self, path):
        """
        Initialize the Module object.

        Parameters
        ----------
        path : str
            Path to the module folder.
        """
        self.path = path
        self.package = self.read_package()
        self.name = self.package.name
        self.create_logs()
        self.doc_path = self.create_docs_path()

    def read_package(self)->Package:
        """Read the package file and create the package object.

        Returns
        -------
        Package Object
        """
        with open(self.path + "/package.json", encoding="utf8") as json_file:
            json_object= json.load(json_file)

        return Package(json_object)

    def create_logs(self):
        """Create the logs file from git logs."""
        repo = git.Git(self.path)
        log_info = repo.log("--merges",  "--all", "--date=local", "--pretty=format:'%ad %d %s'").replace("(HEAD -> master) ", "").replace("'","")
        matches = re.findall(r"\w{3} \w{3} \d\d? \d\d?:\d{2}:\d{2} \d{4}  .*[^Merge branch master]$",log_info, re.MULTILINE)
        if matches:
            lines = "\n".join(matches)
            with open(self.path + "/CHANGES.txt", "w") as f:
                f.write(lines)

    def create_docs_path(self)->str:
        """Create the path to the docs folder. If the folder not exists, it will be created.

        Returns
        -------
        str
            Path to the docs folder.
        """
        docs_folder = os.path.join(self.path, "docs")
        if not os.path.exists(docs_folder):
            os.mkdir(docs_folder)

        return os.path.join(docs_folder, f"Manual_{self.name}")
        
        
if __name__ == '__main__':

    import sys
    from tkinter import filedialog
    from tkinter import messagebox

    argv = sys.argv[1:]
    readme = True
    manual = True
    lang = "es"
    terminal = False
    if len(argv) > 0:
        terminal = True
    folder = argv[-1] if len(argv) > 0 else ""

    if "-m" in argv or "--manual" in argv:
        readme = False
    if "-r" in argv or "--readme" in argv:
        manual = False
    if "-l" in argv:
        lang = argv[argv.index("-l") + 1]
    if  "--lang" in argv:
        lang = argv[argv.index("--lang") + 1]

    if "-h" in argv or "--help" in argv:
        print(__doc__)
        exit()

    if not len(argv) or not os.path.exists(folder) or not os.path.isdir(folder):
        folder = filedialog.askdirectory()

    if not folder:
        exit()
    
    documentator = Documentator(folder)
    # if readme:
    #     documentator.to_readme(lang="en")
    if manual:
        documentator.to_manual(lang=lang)

    if not terminal:
        messagebox.showinfo(message=f"README.md and Manual_{documentator.package.name}.md was created" , title="Success")
        exit()
    
    print(f"README.md and Manual_{documentator.package.name}.md was created")


