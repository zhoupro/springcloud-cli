#!/usr/bin/env python3
""" 初始化 spring boot 项目。

Usage:
  sb.py  module create <module>
  sb.py  project create <groupId> <artifactId>
  sb.py  module delete <module>
  sb.py  deps   add  [<base>]  [<db>] [<kv>] [<mq>]
  sb.py  deps   list
  sb.py  path   init
  sb.py  main   init
  sb.py  res    init
  sb.py  autogen
  sb.py  advice time
  sb.py  jsonres
  sb.py  json2dto
  sb.py  mq   kafka  add
"""

from docopt import docopt
import os
import xml.etree.ElementTree as ET
import shutil

ns = {'pom4': 'http://maven.apache.org/POM/4.0.0',
      'role': 'http://characters.example.com'}

sb_project = os.path.dirname(__file__)

def pretty_xml(element, indent, newline, level=0):  # elemnt为传进来的Elment类，参数indent用于缩进，newline用于换行
    if element:  # 判断element是否有子元素
        if (element.text is None) or element.text.isspace():  # 如果element的text没有内容
            element.text = newline + indent * (level + 1)
        else:
            element.text = newline + indent * (level + 1) + element.text.strip() + newline + indent * (level + 1)
            # else:  # 此处两行如果把注释去掉，Element的text也会另起一行
            # element.text = newline + indent * (level + 1) + element.text.strip() + newline + indent * level
    temp = list(element)  # 将element转成list
    for subelement in temp:
        if temp.index(subelement) < (len(temp) - 1):  # 如果不是list的最后一个元素，说明下一个行是同级别元素的起始，缩进应一致
            subelement.tail = newline + indent * (level + 1)
        else:  # 如果是list的最后一个元素， 说明下一行是母元素的结束，缩进应该少一个
            subelement.tail = newline + indent * level
        pretty_xml(subelement, indent, newline, level=level + 1)

springboot2parent =  {
            "groupId": "org.springframework.boot",
            "artifactId": "spring-boot-starter-parent",
            "version": "2.3.12.RELEASE",
        }


springboot2dependencyManage = [

    {
        "groupId": "org.springframework.cloud",
        "artifactId": "spring-cloud-dependencies",
        "version": "Hoxton.SR12",
        "type": "pom",
        "scope": "import"
    },

    {
        "groupId": "com.alibaba.cloud",
        "artifactId": "spring-cloud-alibaba-dependencies",
        "version": "2.2.6.RELEASE",
        "type": "pom",
        "scope": "import"
    },

    {
        "groupId": "org.projectlombok",
        "artifactId": "lombok",
        "version": "1.18.28"
    },


    {
        "groupId": "org.springframework.boot",
        "artifactId": "mybatis-spring-boot-starter",
        "version": "3.0.1",
    },

    {
        "groupId": "mysql",
        "artifactId": "mysql-connector-java",
        "version": "8.0.25",
        "comment": "MySql 驱动, mybatis依赖该包"
    },

    {
        "groupId": "org.mybatis",
        "artifactId": "mybatis",
        "version": "3.5.11",
        "comment": "mybatis 核心包"
    },

    {
        "groupId": "com.baomidou",
        "artifactId": "mybatis-plus-boot-starter",
        "version": "3.5.3.1",
        "comment": "mybatis plus 核心包"
    },
    {
        "groupId": "com.baomidou",
        "artifactId": "mybatis-plus-generator",
        "version": "3.5.3.1",
        "comment":"mybatis-plus-generator 核心包，CRUD代码生成器"
    },

    {
        "groupId": "org.apache.velocity",
        "artifactId": "velocity-engine-core",
        "version": "2.3",
        "comment": "模板引擎， mybatis-plus-generator 依赖"
    },

    {
        "groupId": "cn.hutool",
        "artifactId": "hutool-all",
        "version": "5.8.22",
        "comment": "hutool 核心包"
    },
    {
            "groupId": "com.github.davidfantasy",
            "artifactId": "mybatis-plus-generator-ui",
            "version": "2.0.5",
            "comment": "mybatis-plus-generator-ui 核心包"
    },

]

springboot2deps = {

    "base": [
        {
            "groupId": "org.springframework.boot",
            "artifactId": "spring-boot-starter-test",
        },

        {
            "groupId": "org.springframework.boot",
            "artifactId": "spring-boot-starter-web",
        },

        {
            "groupId": "org.springframework.boot",
            "artifactId": "spring-boot-starter-aop",
            "exclusions": [
                {
                    "groupId": "org.springframework.boot",
                    "artifactId": "spring-boot-starter-logging",
                }
            ],
        },

        {
            "groupId": "com.alibaba.cloud",
            "artifactId": "spring-cloud-starter-alibaba-nacos-discovery",
        },

        {
            "groupId": "com.alibaba.cloud",
            "artifactId": "spring-cloud-starter-alibaba-nacos-config",
        },

        {
            "groupId": "org.springframework.boot",
            "artifactId": "spring-boot-starter-log4j2",
        },

        {
            "groupId": "org.springframework.cloud",
            "artifactId": "spring-cloud-starter-sleuth",
        },

        {
            "groupId": "org.projectlombok",
            "artifactId": "lombok",
        },


    ],

    "db": [
        {
            "groupId": "mysql",
            "artifactId": "mysql-connector-java",
        },

        {
            "groupId": "org.mybatis",
            "artifactId": "mybatis",
        },

        {
            "groupId": "com.baomidou",
            "artifactId": "mybatis-plus-boot-starter",
        },
        {
            "groupId": "com.baomidou",
            "artifactId": "mybatis-plus-generator",
        },

        {
            "groupId": "org.apache.velocity",
            "artifactId": "velocity-engine-core",
        },
        {
            "groupId": "com.github.davidfantasy",
            "artifactId": "mybatis-plus-generator-ui",
            "scope": "test",
        },

    ],
    "kv": [
         {
            "groupId": "org.springframework.boot",
            "artifactId": "spring-boot-starter-data-redis",
        },
        {
            "groupId": "org.apache.commons",
            "artifactId": "commons-pool2",
        },
    ],

    "mq": [
        {
            "groupId": "org.springframework.kafka",
            "artifactId": "spring-kafka",
        }
    ]

}





def makeProject(groupId, artifactId):

    if not os.path.exists(artifactId):
        os.mkdir(artifactId)

    oldPwd = os.getcwd()
    os.chdir(artifactId)

    if not os.path.exists("./pom.xml"):
        shutil.copy(sb_project + "/temps/project-pom.xml", "./pom.xml")



    import xml.etree.ElementTree as ET
    # 加载POM文件
    tree = ET.parse('pom.xml')
    ns = "http://maven.apache.org/POM/4.0.0"
    ET.register_namespace('', ns)
    root = tree.getroot()
    groupIdNode = root.find("{http://maven.apache.org/POM/4.0.0}groupId")
    groupIdNode.text = groupId
    artifactIdNode = root.find("{http://maven.apache.org/POM/4.0.0}artifactId")
    artifactIdNode.text = artifactId

    parent = root.find("{http://maven.apache.org/POM/4.0.0}parent")

    if parent == None:
        # parent
        parent = ET.Element('parent')
        groupId = ET.SubElement(parent, 'groupId')
        groupId.text = springboot2parent.get("groupId")
        artifactId = ET.SubElement(parent, 'artifactId')
        artifactId.text = springboot2parent.get("artifactId")
        version = ET.SubElement(parent, 'version')
        version.text = springboot2parent.get("version")
        root.insert(5, parent)

    dependencyManagement = root.find("{http://maven.apache.org/POM/4.0.0}dependencyManagement")

    if dependencyManagement == None:
        #dependency
        dependencyManagement = ET.Element('dependencyManagement')
        dependencies = ET.SubElement(dependencyManagement, 'dependencies')
        for dep in springboot2dependencyManage:
            dependency = ET.SubElement(dependencies, 'dependency')
            groupId = ET.SubElement(dependency, 'groupId')
            groupId.text = dep.get("groupId")
            artifactId = ET.SubElement(dependency, 'artifactId')
            artifactId.text = dep.get("artifactId")
            version = ET.SubElement(dependency, 'version')
            version.text = dep.get("version")
            if dep.get("type", "") != "":
                type = ET.SubElement(dependency, 'type')
                type.text = dep.get("type")
            if dep.get("scope", "") != "":
                scope = ET.SubElement(dependency, 'scope')
                scope.text = dep.get("scope")

        if len(springboot2dependencyManage) > 0 :
            root.insert(5, dependencyManagement)

    pretty_xml(root, '\t', '\n')
    tree.write('pom.xml', encoding="utf-8", xml_declaration=True)
    os.chdir(oldPwd)


def getProjectInfo(pomxml):
    import xml.etree.ElementTree as ET
    # 加载POM文件
    tree = ET.parse(pomxml)
    root = tree.getroot()
    version = root.find("{http://maven.apache.org/POM/4.0.0}version")
    groupId = root.find("{http://maven.apache.org/POM/4.0.0}groupId")
    artifactId = root.find("{http://maven.apache.org/POM/4.0.0}artifactId")
    # 获取项目信息
    return {

        "version": version.text,
        "groupId": groupId.text,
        "artifactId": artifactId.text
    }

def getModuleInfo(pomxml):
    import xml.etree.ElementTree as ET
    # 加载POM文件
    tree = ET.parse(pomxml)
    root = tree.getroot()
    artifactId = root.find("{http://maven.apache.org/POM/4.0.0}artifactId")
    # 获取项目信息
    return {
        "artifactId": artifactId.text
    }

def isProject(pomxml):
    import xml.etree.ElementTree as ET
    # 加载POM文件
    tree = ET.parse(pomxml)
    root = tree.getroot()
    packaging = root.find("{http://maven.apache.org/POM/4.0.0}packaging")
    return packaging != None and packaging.text == "pom"

def addModuleToProject(moduleName,pwd):
    import xml.etree.ElementTree as ET
    # 加载POM文件
    tree = ET.parse(pwd+"/pom.xml")
    ns = "http://maven.apache.org/POM/4.0.0"
    ET.register_namespace('', ns)
    root = tree.getroot()
    modules = root.find("{http://maven.apache.org/POM/4.0.0}modules")
    if modules == None:
        parent = ET.Element('modules')
        groupId = ET.SubElement(parent, 'module')
        groupId.text = moduleName
        root.insert(5, parent )
    else:
        findFlag = False
        for m in modules:
            if m.text == moduleName:
                print("exist module")
                findFlag = True
                break
        if findFlag == False:
            module = ET.Element('module')
            module.text = moduleName
            modules.append(module)

    pretty_xml(root, '\t', '\n')
    tree.write('pom.xml', encoding="utf-8", xml_declaration=True)



def makeModule( artifactId, pwd ):
    if os.path.exists(pwd + "/" + artifactId):
        print(" module exist")
        return
    if not isProject(pwd+"/pom.xml"):
        print("current dir is not project")
        return
    if not os.path.exists(pwd+"/"+artifactId):
        addModuleToProject(artifactId, pwd)

    targetPath = pwd + "/" +artifactId
    if not os.path.exists(targetPath):
        os.makedirs(targetPath, exist_ok=True)
    oldPwd = pwd
    os.chdir(artifactId)


    if not os.path.exists("./pom.xml"):
        shutil.copy(sb_project+ "/temps/module-pom.xml", "./pom.xml")


    parentInfo = getProjectInfo("../pom.xml")
    parentGroupId = parentInfo.get("groupId")
    parentArtifactId = parentInfo.get("artifactId")
    parentVersion = parentInfo.get("version")

    import xml.etree.ElementTree as ET
    # 加载POM文件
    tree = ET.parse('pom.xml')
    ns = "http://maven.apache.org/POM/4.0.0"
    ET.register_namespace('', ns)
    root = tree.getroot()
    artifactIdNode = root.find("{http://maven.apache.org/POM/4.0.0}artifactId")
    artifactIdNode.text = artifactId

    parentNode = root.find("{http://maven.apache.org/POM/4.0.0}parent")
    if parentNode == None:
        parent = ET.Element('parent')
        groupId = ET.SubElement(parent, 'groupId')
        groupId.text = parentGroupId
        artifactId = ET.SubElement(parent, 'artifactId')
        artifactId.text = parentArtifactId
        version = ET.SubElement(parent, 'version')
        version.text = parentVersion
        root.insert(2, parent)

    pretty_xml(root, '\t', '\n')
    tree.write('pom.xml', encoding="utf-8", xml_declaration=True)
    os.chdir(oldPwd)


def addDepsToModule( addSets ):
    import xml.etree.ElementTree as ET
    # 加载POM文件
    tree = ET.parse('pom.xml')
    ns = "http://maven.apache.org/POM/4.0.0"
    ET.register_namespace('', ns)
    root = tree.getroot()
    packaging = root.find("{http://maven.apache.org/POM/4.0.0}packaging")
    if packaging != None and packaging.text == "pom":
        print("need in modules")
        return
    depSets = []
    if addSets.get("base", False):
        depSets = springboot2deps["base"]
    if addSets.get("kv",False) :
        depSets += springboot2deps["kv"]

    if addSets.get("db",False) :
        depSets += springboot2deps["db"]

    if addSets.get("mq",False):
        depSets += springboot2deps["mq"]

    import xml.etree.ElementTree as ET
    # 加载POM文件
    tree = ET.parse('pom.xml')
    ns = "http://maven.apache.org/POM/4.0.0"
    ET.register_namespace('', ns)
    root = tree.getroot()
    dependencies = root.find("{http://maven.apache.org/POM/4.0.0}dependencies")
    addFlag = False
    if dependencies == None:
        addFlag = True
        dependencies = ET.Element('dependencies')

    existDepSets = findDepsByPath("dependencies/dependency")
    for dep in depSets:
        uniqKey = dep.get("groupId") + ":" + dep.get("artifactId")
        if uniqKey in existDepSets:
            print( "has added " + uniqKey )
            continue
        else:
            print("is adding " + uniqKey  )
        # dependency
        dependency =ET.Element('dependency')
        groupId = ET.SubElement(dependency, 'groupId')
        groupId.text = dep.get("groupId")
        artifactId = ET.SubElement(dependency, 'artifactId')
        artifactId.text = dep.get("artifactId")
        if dep.get("scope", None) != None:
            scope = ET.SubElement(dependency, 'scope')
            scope.text = dep.get("scope")

        if dep.get("exclusions", None) != None:
            exclusions = ET.SubElement(dependency, 'exclusions')
            for e in dep.get("exclusions"):
                exclusion = ET.SubElement(exclusions, 'exclusion')
                groupId = ET.SubElement(exclusion, 'groupId')
                groupId.text = e.get("groupId")
                artifactId = ET.SubElement(exclusion, 'artifactId')
                artifactId.text = e.get("artifactId")

        dependencies.append( dependency)

    if len(depSets) > 0 and addFlag:

        root.insert(3, dependencies)

    pretty_xml(root, '\t', '\n')
    tree.write('pom.xml', encoding="utf-8", xml_declaration=True)

def findDepsByPath(findPath):
    prefix = "{http://maven.apache.org/POM/4.0.0}"

    findPathInfo = findPath.split("/")
    findFullPath = ""
    for fp in findPathInfo:
        findFullPath = findFullPath +  prefix + fp + "/"
    findFullPath = findFullPath.rstrip("/")
    import xml.etree.ElementTree as ET
    # 加载POM文件
    tree = ET.parse('pom.xml')
    ns = "http://maven.apache.org/POM/4.0.0"
    ET.register_namespace('', ns)
    root = tree.getroot()
    dependencies = root.findall(findFullPath)
    depSets = set()
    if dependencies == None:
        return depSets
    for dep in dependencies:
        depSets.add(dep[0].text + ":" + dep[1].text)
    return depSets


def listDepsOfModule(findPath):
    depSets=findDepsByPath(findPath)
    for dep in depSets:
        print(dep)

def pathInit(pwd):
    if not isProject("../pom.xml"):
        print("not in modules")
        return

    projectInfo = getProjectInfo("../pom.xml")
    groupId = projectInfo["groupId"]
    pathList = ["src/main/java", "src/test/java"]
    groupIdPath = groupId.split(".")

    pathFullList = []

    for p in pathList:
        for gp in groupIdPath:
            p = p + "/" + gp
        pathFullList += [p]

    pathFullList += [ "src/main/resources",  "src/test/resources" ]

    for p in pathFullList:
        if  not os.path.exists(pwd + "/" + p):
            os.makedirs(pwd + "/" + p)


def mainInit(pwd):
    if not isProject("../pom.xml"):
        print("not in modules")
        return

    projectInfo = getProjectInfo("../pom.xml")
    groupId = projectInfo["groupId"]

    groupIdInfo = groupId.split(".")

    moduleInfo = getModuleInfo("./pom.xml")
    artifactId = moduleInfo["artifactId"]

    artifactId = artifactId.capitalize()

    from jinja2 import Template
    bootstrapStr = open(sb_project + "/" + "temps/bootstrap.java").read()
    template = Template(bootstrapStr)
    print()
    targetFile = pwd + "/" + "src/main/java"
    for g in groupIdInfo:
        targetFile = targetFile + "/" + g

    targetFile = targetFile + "/" + artifactId + "Main.java"
    f = open(targetFile, "w")
    f.write(template.render(packageName=groupId, className= artifactId + "Main"))
    f.close()

def resInit(pwd):
    if not isProject("../pom.xml"):
        print("not in modules")
        return


    moduleInfo = getModuleInfo("./pom.xml")
    artifactId = moduleInfo["artifactId"]

    if not os.path.exists(pwd + "/src/main/resources/log4j2/log4j2-dev.xml"):
        print("init log4j2")
        print(pwd + "/src/main/resources/log4j2/")
        os.makedirs(pwd + "/src/main/resources/log4j2/", exist_ok=True)
        shutil.copy(sb_project + "/temps/resources/log4j2/log4j2-dev.xml", pwd + "/src/main/resources/log4j2/log4j2-dev.xml")

    if not os.path.exists(pwd + "/" + "src/main/resources/bootstrap.yml"):
        shutil.copy(sb_project + "/" + "temps/resources/bootstrap.yml", pwd + "/" + "src/main/resources/bootstrap.yml")
    else:
        print("res already init")
        return

    from jinja2 import Template
    bootstrapStr = open(sb_project + "/" + "temps/resources/bootstrap-dev.yml").read()
    template = Template(bootstrapStr)
    targetFile = pwd + "/" + "src/main/resources/bootstrap-dev.yml"

    f = open(targetFile, "w")
    f.write(template.render( artifactId= artifactId))
    f.close()

def autoInit(pwd):
    if not isProject("../pom.xml"):
        print("not in modules")
        return

    projectInfo = getProjectInfo("../pom.xml")
    groupId = projectInfo["groupId"]

    groupIdInfo = groupId.split(".")


    from jinja2 import Template
    bootstrapStr = open(sb_project + "/" + "temps/test/AutoGenTest.java").read()
    template = Template(bootstrapStr)
    targetFile = pwd + "/" + "src/test/java"
    for g in groupIdInfo:
        targetFile = targetFile + "/" + g

    targetFile = targetFile + "/autogen/"
    os.makedirs(targetFile, exist_ok=True)
    targetFile = targetFile  + "AutoGenTest.java"
    f = open(targetFile, "w")
    f.write(template.render(packageName=groupId))
    f.close()

def adviceInit(pwd):
    if not isProject("../pom.xml"):
        print("not in modules")
        return

    projectInfo = getProjectInfo("../pom.xml")
    groupId = projectInfo["groupId"]

    groupIdInfo = groupId.split(".")

    from jinja2 import Template
    bootstrapStr = open(sb_project + "/" + "temps/advice/ExecutionTimeAdvice.java").read()
    template = Template(bootstrapStr)
    targetFile = pwd + "/" + "src/main/java"
    for g in groupIdInfo:
        targetFile = targetFile + "/" + g

    targetFile = targetFile + "/advice/"
    os.makedirs(targetFile, exist_ok=True)
    targetFile = targetFile  + "ExecutionTimeAdvice.java"
    f = open(targetFile, "w")
    f.write(template.render(packageName=groupId))
    f.close()

def kafkaInit(pwd):
    if not isProject("../pom.xml"):
        print("not in modules")
        return

    projectInfo = getProjectInfo("../pom.xml")
    groupId = projectInfo["groupId"]

    groupIdInfo = groupId.split(".")

    # 新增 kafka pom 依赖
    addSets = {}
    addSets["mq"] = True
    addDepsToModule(addSets)

    fileList = [
        "consumer/Consumer.java",
        "services/KafkaProcucer.java",
    ]

    commonPath = pwd + "/" + "src/main/java"
    for g in groupIdInfo:
        commonPath = commonPath + "/" + g

    for f in fileList:
        fInfo = f.split("/")
        from jinja2 import Template
        bootstrapStr = open(sb_project + "/" + "temps/"+ f).read()
        template = Template(bootstrapStr)
        targetFile = commonPath + "/"+ fInfo[0] +"/"
        os.makedirs(targetFile, exist_ok=True)
        targetFile = targetFile  + fInfo[1]
        f = open(targetFile, "w")
        f.write(template.render(packageName=groupId))
        f.close()

def jsonResInit(pwd):
    if not isProject("../pom.xml"):
        print("not in modules")
        return

    projectInfo = getProjectInfo("../pom.xml")
    groupId = projectInfo["groupId"]

    groupIdInfo = groupId.split(".")

    fileList = [
        "advice/GlobalExceptionAdvice.java",
        "advice/ResponseAdvice.java",
        "advice/NotControllerResponseAdvice.java",
        "enums/ResultCode.java",
        "exception/BizException.java",
        "vo/Result.java"
    ]

    commonPath = pwd + "/" + "src/main/java"
    for g in groupIdInfo:
        commonPath = commonPath + "/" + g

    for f in fileList:
        fInfo = f.split("/")
        from jinja2 import Template
        bootstrapStr = open(sb_project + "/" + "temps/"+ f).read()
        template = Template(bootstrapStr)
        targetFile = commonPath + "/"+ fInfo[0] +"/"
        os.makedirs(targetFile, exist_ok=True)
        targetFile = targetFile  + fInfo[1]
        f = open(targetFile, "w")
        f.write(template.render(packageName=groupId))
        f.close()


def jsonDtoInit(pwd):
    if not isProject("../pom.xml"):
        print("not in modules")
        return

    projectInfo = getProjectInfo("../pom.xml")
    groupId = projectInfo["groupId"]

    if not os.path.exists(pwd + "/src/main/resources/json2dto"):
        print("init json2dto")
        print(pwd + "/src/main/resources/json2dto/")
        os.makedirs(pwd + "/src/main/resources/json2dto/", exist_ok=True)
        shutil.copytree(sb_project + "/temps/resources/json2dto", pwd + "/src/main/resources/json2dto", dirs_exist_ok=True)

    xml_string = """
        <plugin>
                <groupId>org.jsonschema2pojo</groupId>
                <artifactId>jsonschema2pojo-maven-plugin</artifactId>
                <version>1.2.1</version>
                <configuration>
                    <sourceType>json</sourceType>
                    <sourceDirectory>${{basedir}}/src/main/resources/json2dto</sourceDirectory>
                    <outputDirectory>${{basedir}}/src/main/java</outputDirectory>
                    <targetPackage>{packageName}.dto</targetPackage>
                    <addCompileSourceRoot>true</addCompileSourceRoot>
                    <annotationStyle>jackson2</annotationStyle>
                    <serializable>true</serializable>
                    <useBigDecimals>true</useBigDecimals>
                    <removeOldOutput>false</removeOldOutput>
                    <includeToString>false</includeToString>
                    <includeHashcodeAndEquals>false</includeHashcodeAndEquals>
                    <includeAdditionalProperties>false</includeAdditionalProperties>
                </configuration>
                <executions>
                    <execution>
                        <goals>
                            <goal>generate</goal>
                        </goals>
                    </execution>
                </executions>
            </plugin>
    """
    xml_string = xml_string.format(packageName = groupId, basedir = "basedir")
    pluginElement = ET.fromstring(xml_string)
    tree = ET.parse('pom.xml')
    ns = "http://maven.apache.org/POM/4.0.0"
    ET.register_namespace('', ns)
    root = tree.getroot()
    plugins = root.find("{http://maven.apache.org/POM/4.0.0}build/{http://maven.apache.org/POM/4.0.0}plugins")
    plugins.append(pluginElement)
    pretty_xml(root, '\t', '\n')
    tree.write('pom.xml', encoding="utf-8", xml_declaration=True)

if __name__ == '__main__':
    arguments = docopt(__doc__.format(filename=os.path.basename(__file__)))
    cmd_root = os.getcwd()

    if arguments.get("module"):
        if arguments.get("create"):
            makeModule(arguments.get("<module>"), cmd_root)

    if arguments.get("project"):
        if arguments.get("create"):
            makeProject(arguments.get("<groupId>"), arguments.get("<artifactId>"))

    if arguments.get("deps"):
        if arguments.get("add"):
            addSets = {}
            if arguments.get("<base>") != None:
                addSets["base"] = True
            if arguments.get("<db>") != None:
                addSets["db"] = True
            if arguments.get("<kv>") != None:
                addSets["kv"] = True
            if arguments.get("<mq>") != None:
                addSets["mq"] = True
            addDepsToModule(addSets)
        if arguments.get("list"):
            listDepsOfModule("dependencies/dependency")

    if arguments.get("path"):
        if arguments.get("init"):
            pathInit(cmd_root)

    if arguments.get("main"):
        if arguments.get("init"):
            mainInit(cmd_root)

    if arguments.get("res"):
        if arguments.get("init"):
            resInit(cmd_root)

    if arguments.get("autogen"):
        autoInit(cmd_root)

    if arguments.get("advice"):
        if arguments.get("time"):
            adviceInit(cmd_root)

    if arguments.get("jsonres"):
        jsonResInit(cmd_root)
    if arguments.get("json2dto"):
        jsonDtoInit(cmd_root)
    if arguments.get("mq"):
        if arguments.get("kafka"):
            if arguments.get("add"):
                kafkaInit(cmd_root)
