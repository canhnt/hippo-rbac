from lxml import etree

__author__ = 'Canh Ngo <https://github.com/canhnt/>'
__version__ = "0.1.0"
__license__ = "Apache License v2.0"


class HippoRole:

    def __init__(self, roleNode):
        self.permissions=[]
        self.name = roleNode.get("id")
        self.inheritsFrom = roleNode.get("inheritsFrom")

        # for pTag in roleNode.xpath("//Permission"):

        for pTag in roleNode.findall("Permission"):
            # print pTag.find("ResourceDomain").text
            resource = pTag.find("ResourceDomain").text
            action = pTag.find("Action").text
            p = HippoPermission(resource, action)
            self.addPermission(p)

    def getName(self):
        return self.name

    def addPermission(self, permission):
        self.permissions.append(permission)

    def getPermissions(self):
        return self.permissions

    def getInheritsFrom(self):
        return self.inheritsFrom

class HippoPermission:
    def __init__(self, resource, action):
        self.resource = resource
        self.action = action

    def getAction(self):
        return self.action

    def getResource(self):
        return self.resource

class RoleReader:

    def _load(self, xmlFile):
        parser = etree.XMLParser()
        doc = etree.parse(xmlFile, parser)

        roles = {}
        for rTag in doc.findall("Role"):
            r = HippoRole(rTag)
            roles.update({r.name : r})

        # Process roles with inheritsFrom attribute
        roles = self.parseInheritance(roles)

        return roles

    def parseInheritance(self, roles):
        for roleName, role in roles.items():
            if role.inheritsFrom:
                baseRole = role.inheritsFrom
                role.permissions.extend(roles[baseRole].permissions)

        return roles


g = RoleReader()
roles = g._load("policies/roles.xml")
print "All permissions:"

for name, role in roles.items():
    print "Role %s:" % name
    for p in role.getPermissions():
        print "\t %s : %s" % (p.resource, p.action)