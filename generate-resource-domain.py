STRING = "String"
BOOLEAN = "Boolean"
NAME_TYPE = "Name"
FACETRULE = "hipposys:facetrule"
HIPPOSYS_DOMAINRULE = "hipposys:domainrule"
HIPPOSYS_DOMAIN = "hipposys:domain"
JCR_PRIMARY_TYPE = "jcr:primaryType"
__author__ = 'canhnt'

from lxml import etree

def createPropertyNode(parent, nodeName, nodeType, nodeValue):
    subNode = etree.SubElement(parent, "property")
    subNode.set("name", nodeName)
    subNode.set("type", nodeType)
    etree.SubElement(subNode, "value").text = nodeValue
    return subNode

# Create a domain rule for each folder in the path
def createFacetRule(parentNode, facet, type, value):
    facetNode = etree.SubElement(parentNode, "node")
    if facet=="jcr:uuid":
        nodeName = "node-by-uuid"
    else:
        nodeName = "node-by-path"

    facetNode.set("name", nodeName)
    createPropertyNode(facetNode, JCR_PRIMARY_TYPE, NAME_TYPE, FACETRULE)
    createPropertyNode(facetNode, "hipposys:equals", BOOLEAN, "true")
    createPropertyNode(facetNode, "hipposys:facet", STRING, facet)
    createPropertyNode(facetNode, "hipposys:filter", BOOLEAN, "false")
    createPropertyNode(facetNode, "hipposys:type", STRING, type)
    createPropertyNode(facetNode, "hipposys:value", STRING, value)
    return facetNode


def createDomainRule(parentNode, facet, type, path):
    folders = filter(None, path.split("/"))
    domainName = "-".join(folders)

    domainRule = etree.SubElement(parentNode, "node")
    domainRule.set("name", "%s-node" % domainName)
    createPropertyNode(domainRule, JCR_PRIMARY_TYPE, NAME_TYPE, HIPPOSYS_DOMAINRULE)
    createFacetRule(domainRule, facet, type, path)

document_path = "/content/document/ggzcentraal/webshop/construction"
paths = filter(None, document_path.split("/"))

JCR_NAMESPACE = "http://www.jcp.org/jcr/sv/1.0"
DELIMITER = "-"
JCR = "{%s}" % JCR_NAMESPACE
NSMAP = {None : JCR_NAMESPACE}

rootNode = etree.Element(JCR + "node", nsmap=NSMAP)

# Set domain rule type
rootNode.set("name", DELIMITER.join(paths))
propertyNode = createPropertyNode(rootNode, JCR_PRIMARY_TYPE, NAME_TYPE, HIPPOSYS_DOMAIN)

# Create jcr:uuid domain rule for parent folders
for index in range(1,len(paths)-1):
    folder = paths[index]
    path = "/" + "/".join(paths[0:index])
    domainRule = createDomainRule(rootNode, "jcr:uuid", "Reference", path)

# Create hippo:paths for the last folder
path = "/" + "/".join(paths)
createDomainRule(rootNode, "hippo:paths", "Reference", path)

print(etree.tostring(rootNode, pretty_print=True))

