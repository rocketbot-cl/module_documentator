import json
import os
from mdutils.mdutils import MdUtils


LICENSES = {
    "MIT": {
        "url": "http://opensource.org/licenses/mit-license.ph",
        "image": "https://camo.githubusercontent.com/107590fac8cbd65071396bb4d04040f76cde5bde/687474703a2f2f696d672e736869656c64732e696f2f3a6c6963656e73652d6d69742d626c75652e7376673f7374796c653d666c61742d737175617265"
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
        
    def get_attribute(self, object, name, lang):
        
        if lang in object:
            return object[lang][name]
        if name in object and isinstance(object[name], dict):
            return object[name][lang]
        if name in object:
            return object[name]
        return ""
        
class Documentator:

    def __init__(self, module_path: str):
        self.path = module_path
        self.name = self.path.split('/')[-1]
        self.package = self.read_package()

    def read_package(self)->Package:
        with open(self.path + "/package.json", encoding="utf8") as json_file:
            json_object= json.load(json_file)

        return Package(json_object)

    def create_md_base(self, path_to_save: str, lang:str)->MdUtils:
        md_file = MdUtils(file_name=path_to_save)
        md_file.new_header(level=1, title=self.package.title[lang])
        self.add_description_module(md_file, self.package.description, lang)
    
        return md_file

    def to_readme(self, path_to_save="README", lang="es", comments="")->None:
        md_file = self.create_md_base(path_to_save, lang)
        md_file.new_header(level=2, title="Overview")
        if comments:
            md_file.new_paragraph(comments)
        for i, command in enumerate(self.package.children, start=1):
            title = self.package.get_attribute(command, "title", lang)
            description = self.package.get_attribute(command, "description", lang)
            md_file.new_paragraph(f"{i}. #### {title}")
            md_file.new_line(description)
            self.add_command_image(md_file, command["module"])
        
        md_file.new_paragraph("----")
        md_file.new_header(level=3, title="OS")
        md_file.new_list(self.package.os)
        md_file.new_header(level=3, title="Dependencies")
        self.add_dependencies(md_file, self.package.dependencies)

        md_file.new_header(level=3, title="License")
        self.add_license(md_file, self.package.license)
        md_file.create_md_file()

    def add_description_module(self, md: MdUtils, description: str, lang: str)->None:
        desc_splitted = description.split("| ")
        if lang == "es":
            description = desc_splitted[0]
        if lang == "en":
            description = desc_splitted[1]
        md.new_line(description.strip())
        md.new_line()

    def add_command_image(self, md: MdUtils, module_name: str)->None:
        image_path = f"example/{module_name}.png"
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

    def to_manual(self, path_to_save="", lang="es"):
        if not path_to_save:
            path_to_save = f"Manual_{self.name}"
        md_file = self.create_md_base(path_to_save, lang)
        for command in self.package.children:
            title = self.package.get_attribute(command, "title", lang)
            description = self.package.get_attribute(command, "description", lang)
            md_file.new_header(level=2, title=title)
            md_file.write(description)
            md_file.new_header(3, "inputs")
            table = ["Input", "Description", "example"]
            for input in command["form"]["inputs"]:
                table.extend([
                    self.package.get_attribute(input, "title", lang).replace(":", ""),
                    "add description here",
                    self.package.get_attribute(input, "placeholder", lang),
                ])
            md_file.new_table(columns=3, rows=len(table)//3, text=table, text_align='center')
        md_file.create_md_file()
        


if __name__ == '__main__':

    documentator = Documentator("C:/Users/danil/Documents/Rocketbot/modules/XML")
    comments = """>The XML command supports sessions and node editing, based on a tree structure of an XML document.\n
The XML command enables users to capture data that has XML formatting and save it to a specified location."""
    documentator.to_readme("Example_Markdown", "en", comments=comments)
    documentator.to_manual()


