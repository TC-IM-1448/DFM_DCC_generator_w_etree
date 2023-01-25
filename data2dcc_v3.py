import shutil as su
from lxml import etree
import xml.etree.ElementTree as ET
from datetime import datetime
import copy
# import xlsxwriter
# import xlrd
import openpyxl as pyxl
import pandas as pd



class DCC:

    def __init__(self):

        self.dcc_original_data = None
        self.dcc_modified_data = None

    def xpath_quantity(self):
        pass

    # loading DCC using etree.ElementTree
    def load_dcc(self, file:str) -> etree:

        # parse xml
        try:
            etree.register_namespace(prefix='dcc', uri="https://ptb.de/dcc")
            etree.register_namespace(prefix='si', uri="https://ptb.de/si")
            doc = etree.parse(file)
            print('XML well formed, syntax ok.')
            self.dcc_original_data = doc
            self.dcc_modified_data = self.dcc_original_data
            return etree.tostring(self.dcc_original_data.getroot()).decode()

        # check for file IO error
        except IOError as err:
            print("IOError" + str(err))

        except ValueError as err:
            print("ValueError" + str(err))

        # check for XML syntax errors
        except etree.XMLSyntaxError as err:
            print('XML Syntax Error, see error_syntax.log')
            with open('error_syntax.log', 'w') as error_log_file:
                error_log_file.write(str(err))
            quit()

    def substitute_token_in_dcc(self, token:str, value:str) -> str:
        """
            This function uses xpath to search for the token provided as input,
            and then stubstitutes the text at the found node with the value provided as input.
            return: A string with the full treepath/xpath to the found node.
        """
        root = self.dcc_modified_data.getroot()
        tree = etree.ElementTree(root)
        try:
            xpath_token = f'//*[contains(text(), "§{token}§")]'
            print(token, ": ", len(root.xpath(xpath_token)))

            elms = root.xpath(xpath_token)
            # TODO: Only 1 xpath occurence must be allowed.
            if len(elms) == 1:
                elms[0].text = str(value)
                return(tree.getpath(elms[0]))
            # root.find(xpath_basic_coverageFactor).text = str(result.k_factor)
        except AttributeError as e:
            print("root.find(xpath_basic_coverageFactor).text" + str(e))


    def save_modified_dcc(self, path=None) -> str:
        """
            This functions saves the modified tree to a new file.
        """
        etree.register_namespace('dcc', "https://ptb.de/dcc")
        etree.register_namespace('si', "https://ptb.de/si")
        file_timestamp = datetime.now().strftime("%Y-%m-%d_%H.%M.%S")
        filename = file_timestamp + " DCC modified.xml"
        self.dcc_modified_data.write(filename, encoding="utf8")
        return filename

def validate_new_dcc(dccfilename, xsdfile="dcc.xsd"):
    """
        Check that resulting dcc is valid
    """
    dccxsd = etree.parse(xsdfile) #TODO select the right Schemafile online
    xsd = etree.XMLSchema(dccxsd)
    etree.register_namespace(prefix='dcc', uri="https://ptb.de/dcc")
    etree.register_namespace(prefix='si', uri="https://ptb.de/si")
    newdcc = etree.parse(newfile)
    validation_result = xsd.validate(newdcc)
    if validation_result:
        print("No Error detected during schema validation")
    else:
        print("An ERROR occured during schema validation")
        xsd.assertValid(newdcc)
    root = newdcc.getroot()
    tree = etree.ElementTree(root)
    etree.register_namespace(prefix='dcc', uri="https://ptb.de/dcc")
    etree.register_namespace(prefix='si', uri="https://ptb.de/si")
    xpath_keys ="/dcc:digitalCalibrationCertificate/dcc:comment/si:list/si:label"
    xpath_paths = "/dcc:digitalCalibrationCertificate/dcc:comment/si:list/si:list/si:label"
    ns_dict = {'dcc':"https://ptb.de/dcc", 'si':"https://ptb.de/si"}
    keys = root.xpath(xpath_keys, namespaces=ns_dict)[0].text
    vals = root.xpath(xpath_paths, namespaces=ns_dict)[0].text
    # [print(f"{k} \t {v}") for k,v in zip(keys.split(" "),vals.split(" "))]
    with open("usr_filepaths_out.csv",'w') as f:
        [f.write(f"{k} , {v}\n") for k,v in zip(keys.split(" "),vals.split(" "))]
    return validation_result


if __name__ == "__main__":
    mydcc = DCC()
    # Load dcc-xml-template
    et = mydcc.load_dcc("2022-08-29_DFM_Template_Temperature.xml")
    # load worksheet excel-file with input values for the dcc-xml-file.
    df = pd.read_excel("DFM_Måleskema_v0.2_annonym.xlsx",sheet_name="Sheet1", index_col=1, usecols=[0,1,2])
    d = df.to_dict()['Value']
    xd = df.to_dict()['UserLabel']
    # for each token found in teh worksheet excel-file the noce is found in the xml-template
    # and substituted by the value worksheet excel-file. If there is a user-Label, then the tree-paths is stored for later entry in the xml.
    usr_d = {}
    for k,v in d.items():
        path = mydcc.substitute_token_in_dcc(k, v)
        if not pd.isna(xd[k]):
            usr_d[k] = path
    # mydcc.dcc_modified_data.
    ks, vs = zip(*usr_d.items())
    ks = " ".join(ks)
    vs = " ".join(vs)
    # Insert the stored tree-paths in the comment section of the dcc-xml.
    mydcc.substitute_token_in_dcc(token="DFMXPATH_keys", value=ks)
    mydcc.substitute_token_in_dcc(token="DFMXPATH_xpaths", value=vs)
    # save the data-tree (etree) to an xml-file.
    newfile = mydcc.save_modified_dcc(path="")
    validate_new_dcc(newfile)

