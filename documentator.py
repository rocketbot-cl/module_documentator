import json
from mdutils.mdutils import MdUtils


LICENSES = {
    "MIT": {
        "url": "http://opensource.org/licenses/mit-license.ph",
        "image": "https://camo.githubusercontent.com/107590fac8cbd65071396bb4d04040f76cde5bde/687474703a2f2f696d672e736869656c64732e696f2f3a6c6963656e73652d6d69742d626c75652e7376673f7374796c653d666c61742d737175617265"
    }
}
class Documentator:

    def __init__(self, package):
        self.package = package

    def to_readme(self, path_to_save, lang="es"):
        package = self.package
        md_file = MdUtils(file_name=path_to_save, title=package.title[lang])
        md_file.write(package.description)
        md_file.new_line()
        md_file.new_header(level=1, title="Overview")
        for command in package.children:
            title = package.get_attribute(command, "title", lang)
            description = package.get_attribute(command, "description", lang)
            md_file.new_header(level=2, title=title)
            md_file.write(description)
            md_file.new_header(3, "inputs")
            table = ["Input", "Description", "example"]
            for input in command["form"]["inputs"]:
                table.extend([
                    package.get_attribute(input, "title", lang).replace(":", ""),
                    "add description here",
                    package.get_attribute(input, "placeholder", lang),
                ])
            md_file.new_table(columns=3, rows=len(table)//3, text=table, text_align='center')
        
        md_file.new_header(level=2, title="OS")
        md_file.new_list(package.os)
        md_file.new_header(level=3, title="Dependencies")
        self.add_dependencies(md_file, package.dependencies)

        md_file.new_header(level=3, title="License")
        self.add_license(md_file, package.license)
        md_file.create_md_file()

    def add_dependencies(self, md, dependencies):
        for dependencie in dependencies:
            md.write(
                "- " + md.new_inline_link(link=dependencies[dependencie], text=dependencie, bold_italics_code='b')
            )    

    def add_license(self, md, license):
        text = license
        path = LICENSES[license]["image"]
        url = LICENSES[license]["url"]
        md.new_line(md.new_inline_image(text,path))
        md.new_line(md.new_inline_link(url, text))

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
        

if __name__ == '__main__':

    with open("package.json", encoding="utf8") as json_file:
        json_object= json.load(json_file)
    package = Package(json_object)
    documentator = Documentator(package)
    documentator.to_readme("Example_Markdown")


