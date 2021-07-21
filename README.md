# XML

 Use the XML command to process XML information that is generated from web services and cloud computing applications.
```
  <books>
    <book>
      <author>David</author>
    </book>
    <book>
      <author>Mark</author>
    </book>
  </books>
```
## Overview

>The XML command supports sessions and node editing, based on a tree structure of an XML document. 


The XML command enables users to capture data that has XML formatting and save it to a specified location.


1. #### Load XML Session File
    Specifies the session name and data source (a file or text).
    
    ![xmlsession](example/xmlsession.png)

2. #### End XML Session
    Complements the **Start XML Session** operation by closing an open XML session - Clean memory.

3. #### Insert Node
    Specifies **node name** and value. The location of the node is based on the position of the XPath Expression.
    
    Specifies action if node name is present (Insert It Anyways, Skip It, or Overwrite It) and where to insert node location (Beginning, End, Before Specific child node, or After Specific child node.

    >**Note:** If Before Specific child node or After Specific child node is selected, specify child node name.
    
    ![Insert Node](example/insertNodeXML.png)

4. #### Delete Node
    Deletes a node  from the XML file by specifying the XPath Expression.

5. #### Update Nodes
    Updates nodes in a session at the position that is specified for the XPath Expression.

    **Update Attributes:** Mark the check box to add, update, or delete attributes.

6. #### Get Node(s)
    Retrieves the value(s) of a single or multiple node(s) in the session data by specifying the XPath Expression.
    - **Get Single Node:** Retrieves the value of a single node or attribute from the session data, at the position specified in the XPath expression. The value is assigned to a variable.
    - **Get Multiple Nodes:** Retrieves values from multiple nodes in the session data, using Text value/XPath expression/Specified attribute name, based on the specified XPath expression.


7. #### Get Session Data
    Get the session data to a variable.

8. #### Save XML Data: 
    Save the data to a specified location.
    >The data is saved in an XML file encoded in UTF-8 format.
    

----

### OS:
  - Linux
  - MacOsX
  - Windows

### Dependencies
- [**xmltodict**](https://pypi.org/project/xmltodict/)
        

### License

![MIT](https://camo.githubusercontent.com/107590fac8cbd65071396bb4d04040f76cde5bde/687474703a2f2f696d672e736869656c64732e696f2f3a6c6963656e73652d6d69742d626c75652e7376673f7374796c653d666c61742d737175617265) 

[MIT License](http://opensource.org/licenses/mit-license.ph)
