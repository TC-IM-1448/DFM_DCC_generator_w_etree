# -*- coding: utf-8 -*-
"""
Created on Mon Mar 28 15:17:05 2022

This routine is a modification of:
https://kevinmloeffler.com/2018/07/08/how-to-extract-pdf-file-attachments-using-python-and-pypdf2/
https://gist.github.com/kevinl95/29a9e18d474eb6e23372074deff2df38

@author: David Balslev-Harder
"""

import PyPDF2

def getAttachments(reader):
      """
      Retrieves the file attachments of the PDF as a dictionary of file names
      and the file data as a bytestring.
      :return: dictionary of filenames and bytestrings
      """
      catalog = reader.trailer["/Root"]
      fileNames = catalog['/Names']['/EmbeddedFiles']['/Names']
      attachments = {}
      for f in fileNames:
          if isinstance(f, str):
              name = f
              dataIndex = fileNames.index(f) + 1
              fDict = fileNames[dataIndex].getObject()
              fData = fDict['/EF']['/F'].getData()
              attachments[name] = fData

      return attachments



if __name__ == "__main__":
    import os
    # Check whether the specified path exists or not
    path = "."+os.sep+"extracted_files"
    isExist = os.path.exists(path)
    print(isExist)
    if not isExist:
        # Create a new directory because it does not exist
        os.makedirs(path)
    print(os.path.exists(path))
    fn = "."+os.sep+"eExample.pdf"

    handler = open(fn, 'rb')
    reader = PyPDF2.PdfFileReader(handler, strict=False)

    dictionary = getAttachments(reader)
    print(dictionary)
    for fName, fData in dictionary.items():
        with open(path+os.sep+fName, 'wb') as outfile:
            outfile.write(fData)
