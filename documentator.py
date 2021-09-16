import json
import os
from mdutils.mdutils import MdUtils


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
    }
}

class Package:

    def __init__(self, json_package: dict):
        self.__dict__.update(json_package)
        self.os_supported()
        self.create_dependencies()

    def os_supported(self):
        self.os = []
        if self.windows:
            self.os.append("windows")
        if self.mac:
            self.os.append("mac")
        if self.linux:
            self.os.append("linux")
        if self.docker:
            self.os.append("docker")

    def create_dependencies(self):
        for name in self.dependencies.keys():
            url = f"https://pypi.org/project/{name}/"
            self.dependencies[name] = url
        
    def get_attribute(self, object, name, lang="en"):
        
        if lang in object:
            return object[lang][name] if name in object[lang] else ""
        if name in object and isinstance(object[name], dict):
            if lang in object[name]:
                return object[name][lang]
        if name in object:
            return object[name]
        return ""

    def get_component_type(self, lang="en"):
        component = "module"
        if hasattr(self, "type"):
            component = self.type
        
        return component

class Documentator:

    def __init__(self, module_path: str, banner_path: str=""):
        self.path = module_path
        self.name = self.path.split('/')[-1]
        self.package = self.read_package()

    def read_package(self)->Package:
        with open(self.path + "/package.json", encoding="utf8") as json_file:
            json_object= json.load(json_file)

        return Package(json_object)

    def create_md_base(self, path_to_save: str, lang:str, banner_path: str="")->MdUtils:
        component_type = self.package.get_component_type(lang)
        md_file = MdUtils(file_name=path_to_save)
        md_file.new_header(level=1, title=self.package.title[lang])
        self.add_description_module(md_file, self.package.description, lang)

        if banner_path:
            md_file.new_line(
                md_file.new_inline_image("banner", banner_path)
            )

        #How to install section
        md_file.new_header(level=2, title=LANGUAGE["how_to_install"][lang] + LANGUAGE[component_type][lang])
        md_file.new_line(LANGUAGE["installation"][lang](component_type))
        #How to use section
        md_file.new_header(level=2, title=LANGUAGE["how_to_use"][lang]+ component_type)
        md_file.new_line("Eiusmod veniam ut nisi minim in. Do et deserunt eiusmod veniam sint aliqua nulla adipisicing laboris voluptate fugiat ullamco elit do. Sint amet cillum fugiat excepteur mollit voluptate reprehenderit nisi commodo sint minim.") 
        return md_file

    def to_readme(self, path_to_save="", lang="en", comments="")->None:
        if not path_to_save:
            path_to_save = os.path.join(self.path, "README.md")
        md_file = self.create_md_base(path_to_save, lang)
        md_file.new_header(level=2, title="Overview")
        if comments:
            md_file.new_paragraph(comments)
        for i, command in enumerate(self.package.children, start=1):
            title = self.package.get_attribute(command, "title", lang)
            description = self.package.get_attribute(command, "description", lang)
            md_file.new_paragraph(f"{i}. {title}")
            md_file.new_line(description)
        
        md_file.new_paragraph("----")
        md_file.new_header(level=3, title="OS")
        md_file.new_list(self.package.os)
        md_file.new_header(level=3, title="Dependencies")
        self.add_dependencies(md_file, self.package.dependencies)

        md_file.new_header(level=3, title="License")
        self.add_license(md_file, self.package.license)
        md_file.create_md_file()

    def add_description_module(self, md: MdUtils, description: str, lang: str)->None:
        if "|" not in description:
            description = description + " | " + description

        desc_splitted = description.split("| ")
        if lang == "es":
            description = desc_splitted[0]
        if lang == "en":
            description = desc_splitted[1]
        md.new_line(description.strip())
        md.new_line()

    def add_command_image(self, md: MdUtils, module_name: str, img_folder:str)->None:
        image_path = f"{img_folder}/{module_name}.png"
        if os.path.exists(self.path + "/" + image_path):
            md.new_line(
                md.new_inline_image(module_name, image_path)
            )

    def add_dependencies(self, md: MdUtils, dependencies: dict)->None:
        for dependencie in dependencies:
            md.write(
                "- " + md.new_inline_link(link=dependencies[dependencie], text=dependencie, bold_italics_code='b')
            )    

    def add_license(self, md: MdUtils, license:str)->None:
        text = license
        path = LICENSES[license]["image"]
        url = LICENSES[license]["url"]
        md.new_line(md.new_inline_image(text,path))
        md.new_line(md.new_inline_link(url, text))

    def to_manual(self, path_to_save="", lang="es", banner_path=""):
        
        if not path_to_save:
            path_to_save = self.create_docs_path()

        if not banner_path:
            banner_path = "https://raw.githubusercontent.com/rocketbot-cl/{name}/master/docs/imgs/Banner_{name}.png".format(name=self.name)

        md_file = self.create_md_base(path_to_save, lang, banner_path)
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
            self.add_command_image(md_file, command["module"], "docs")
        md_file.create_md_file()
        
    def create_docs_path(self):
        docs_folder = os.path.join(self.path, "docs")
        if not os.path.exists(docs_folder):
            os.mkdir(docs_folder)

        return os.path.join(docs_folder, f"Manual_{self.name}")
        
        


if __name__ == '__main__':

    from tkinter import filedialog
    from tkinter import messagebox


    folder = filedialog.askdirectory()

    documentator = Documentator(folder)
    documentator.to_readme(lang="en")
    documentator.to_manual()

    messagebox.showinfo(message=f"README.md and Manual_{documentator.package.name}.md was created" , title="Success")


