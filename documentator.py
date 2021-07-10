import json
from mdutils.mdutils import MdUtils

class Documentator:

    def __init__(self, package_path):
        self.package_path = package_path

    def _read_document(self, path):
        with open(path) as json_file:
            return json.load(json_file)

    def to_markdown(self, path_to_save):
        package = self._read_document(self.package_path)



class Package:

    def __init__(self, json_package: dict):
        self.__dict__.update(json_package)
        
    def to_markdown(self, path_to_save, lang="es"):
        md_file = MdUtils(file_name=path_to_save, title=self.title[lang])
        md_file.write(self.description)
        md_file.new_line()
        md_file.new_header(level=1, title="Commands")
        for command in self.children:
            title = self.get_attribute(command, "title", lang)
            description = self.get_attribute(command, "description", lang)
            md_file.new_header(level=2, title=title)
            md_file.write(description)
            md_file.new_header(3, "inputs")
            table = ["Input", "Description", "example"]
            for input in command["form"]["inputs"]:
                table.extend([
                    self.get_attribute(input, "title", lang),
                    "add description here",
                    self.get_attribute(input, "placeholder", lang),
                ])
            md_file.new_table(columns=3, rows=len(table)//3, text=table, text_align='center')
        md_file.create_md_file()

    
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
    package.to_markdown("Example_Markdown")


