from celery.task import task
import requests, os,json
#from subprocess import call,check_output,STDOUT
from commandline import commandLineExec

folioDataLoader_url =os.getenv('folioDataLoader_url',"http://dataloader_folio")
host_url =os.getenv('HOSTURL',"http://okapihost")

@task()
def loadMarcRules(marc_rules=None):
    """
    Load MARC Rules for the bulk data bulk data loader.

    Signature:
        loadMarcRules(json=None)
    kwargs:
        marc_rules - json - default(https://github.com/folio-org/mod-data-loader/blob/master/ramls/rules.json)
    """
    if marc_rules:
        filename = 'rules.json'
        with open('rules.json','w') as f1:
            f1.write(marc_rules)
    else:
        filename='rulesdefault.json'

    url = "{0}:8081/load/marc-rules".format(folioDataLoader_url)
    command = ['curl','-X POST',"-H", "x-okapi-tenant:diku",
                "-H", "Content-Type:application/octet-stream",
                "-d", "@data/{0}".format(filename),url]
    try:
        result=commandLineExec(command)
    except:
        raise
    if result:
        return result
    return "Successful upload of rules"

@task()
def loadMARCdata(test=True,marc_filename=None):
    """
    Load MARC Data from mod-data-loader.

    Signature:
        loadMARCdata(test=True,marc_filename=None)
    kwargs:
        test = True
        marc_filename = None - Default set to sample MARC binary file
    """
    if not marc_filename:
        marc_filename="marc.dat"

    url = "{0}:8081/load/marc-data?storageURL={1}:9139".format(folioDataLoader_url,host_url)
    if test:
        url = "{0}:8081/load/marc-data/test".format(folioDataLoader_url)

    command = ['curl','-X POST',"-H", "x-okapi-tenant:diku",
                "-H", "Content-Type:application/octet-stream",
                "-d", "@data/{0}".format(marc_filename),url]
    print(" ".join(command))
    try:
        result=commandLineExec(command)
    except:
        raise
    if result:
        try:
            temp=[]
            for rec in result.split("\n"):
                data= rec.split('|')[1]
                temp.append(json.loads(data))
            return temp
        except:
            return result
    return "Successful MARC data upload"
