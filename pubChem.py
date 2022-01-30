import requests

def ctor():
    inputFile = open("input.txt", )
    outputFile = open("output.txt", "w")
    outputFile.close()
    outputFile = open("output.txt", "a")
    return inputFile, outputFile

def writeFile(outputFile, line):
    outputFile.write(line + "\n")

def getCid(response):
    try:
        cid = response.json()["PC_Compounds"][0]["id"]["id"]["cid"]
    except:
        cid = "not_found"
    return cid

def getATC(cid):
    atc = "not_found"
    while True:
        try:
            response = requests.get(("https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/compound/{}/JSON/").format(cid))
            break
        except:
            pass
    try:
        for i in response.json()["Record"]["Section"]:
            if "ATC Code" in str(i) and " - " in str(i):
                for j in i["Section"]:
                    if "ATC Code" in str(j) and " - " in str(j):
                        for k in j["Information"]:
                            if "ATC Code" in str(k) and " - " in str(k):
                                for l in k["Value"]["StringWithMarkup"]:
                                    if atc == "not_found":
                                        atc = l["String"].split(" ")[0]
                                    else:
                                        atc = atc + "-" + l["String"].split(" ")[0]
                                break
                        break
                break
    except:
        pass
    return atc

def getSmiles(response, line, outputFile):
    smiles = "not_found"
    try:
        for i in response.json()["PC_Compounds"][0]["props"]:
            if i["urn"]["label"] == "SMILES" and i["urn"]["name"] == "Canonical":
                smiles = i["value"]["sval"]
                break
    except:
        pass

    cid = getCid(response)
    if cid == "not_found":
        atc = "not_found"
    else:
        atc = getATC(cid)

    writeFile(outputFile, (line.replace("\n", "") + "#" + smiles + "#" + atc))

def readFile(inputFile, outputFile):
    for line in inputFile.readlines():
        while True:
            try:
                response = requests.get(("https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/{}/JSON").format(line.replace("\n", "")))
                break
            except:
                pass
        getSmiles(response, line, outputFile)


def dtor(files):
    files[0].close()
    files[1].close()

def main():
    files = ctor()
    readFile(files[0], files[1])
    dtor(files)

if __name__ == '__main__':
    main()
