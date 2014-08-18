#!/usr/bin/env python

from lxml import etree

__author__ = 'Canh Ngo <https://github.com/canhnt/>'
__version__ = "0.1.0"
__license__ = "Apache License v2.0"

STRING_TYPE = "String"
BOOLEAN_TYPE = "Boolean"
NAME_TYPE = "Name"
FACETRULE = "hipposys:facetrule"
HIPPOSYS_DOMAINRULE = "hipposys:domainrule"
HIPPOSYS_DOMAIN = "hipposys:domain"
JCR_PRIMARY_TYPE = "jcr:primaryType"
JCR_NAMESPACE = "http://www.jcp.org/jcr/sv/1.0"
DELIMITER = "-"

JCR_NS = "{%s}" % JCR_NAMESPACE
NSMAP = {"xs" : JCR_NAMESPACE}


def createPropertyNode(parent, nodeName, nodeType, nodeValue):
    subNode = etree.SubElement(parent, _tag = JCR_NS + "property", nsmap = NSMAP)
    subNode.set(JCR_NS + "name", nodeName)
    subNode.set(JCR_NS + "type", nodeType)
    etree.SubElement(_parent = subNode, _tag = JCR_NS + "value", nsmap = NSMAP).text = nodeValue
    return subNode

# Create a domain rule for each folder in the path
def createFacetRule(parentNode, facet, type, value):
    facetNode = etree.SubElement(parentNode, JCR_NS + "node", nsmap = NSMAP)
    if facet=="jcr:uuid":
        nodeName = "node-by-uuid"
    else:
        nodeName = "node-by-path"

    facetNode.set(JCR_NS + "name", nodeName)
    createPropertyNode(facetNode, JCR_PRIMARY_TYPE, NAME_TYPE, FACETRULE)
    createPropertyNode(facetNode, "hipposys:equals", BOOLEAN_TYPE, "true")
    createPropertyNode(facetNode, "hipposys:facet", STRING_TYPE, facet)
    createPropertyNode(facetNode, "hipposys:filter", BOOLEAN_TYPE, "false")
    createPropertyNode(facetNode, "hipposys:type", STRING_TYPE, type)
    createPropertyNode(facetNode, "hipposys:value", STRING_TYPE, value)
    return facetNode


def createDomainRule(parentNode, facet, type, path):
    folders = filter(None, path.split("/"))
    domainName = "-".join(folders)

    domainRule = etree.SubElement(parentNode, JCR_NS + "node", nsmap = NSMAP)
    domainRule.set(JCR_NS + "name", "%s-node" % domainName)
    createPropertyNode(domainRule, JCR_PRIMARY_TYPE, NAME_TYPE, HIPPOSYS_DOMAINRULE)
    createFacetRule(domainRule, facet, type, path)

def createResourceDomain(jcrFolderPath):
    pathElements = filter(None, jcrFolderPath.split("/"))

    rootNode = etree.Element(JCR_NS + "node", nsmap = NSMAP)

    # Set domain rule type
    rootNode.set(JCR_NS + "name", DELIMITER.join(pathElements))
    propertyNode = createPropertyNode(rootNode, JCR_PRIMARY_TYPE, NAME_TYPE, HIPPOSYS_DOMAIN)

    # Create jcr:uuid domain rule for parent folders
    for index in range(1, len(pathElements)-1):
        path = "/" + "/".join(pathElements[0:index])
        domainRule = createDomainRule(rootNode, "jcr:uuid", "Reference", path)

    # Create hippo:paths for the last folder
    path = "/" + "/".join(pathElements)
    createDomainRule(rootNode, "hippo:paths", "Reference", path)
    return rootNode

document_path = "/content/document/ggzcentraal/webshop/construction"
print(etree.tostring(createResourceDomain(document_path), pretty_print=True))