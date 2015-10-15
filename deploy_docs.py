from fabric.api import run, local, cd, lcd, put, settings


def deploy_ccp_docs(ccp_doc_root="public_html/py/netscriptgen", ccp_bundle_name="ccp.tar.gz", doc_host=""):

    with lcd('docs'):
        local('make html')  # local command

    with lcd('docs/_build/html'):
        local('tar cvfz ~/{0} *'.format(ccp_bundle_name))

    with lcd('docs'):
        local('make clean')

    with settings(host_string=doc_host):
        # scp file to server
        put(local_path="~/{0}".format(ccp_bundle_name),
            remote_path=ccp_bundle_name)
        with cd(ccp_doc_root):
            run("rm -rf *")  # Remote command
            run("mv ~/{0} .".format(ccp_bundle_name))
            run("tar xvfz {0}".format(ccp_bundle_name))
            run("rm {0}".format(ccp_bundle_name))

if __name__ == "__main__":
    doc_host_input = input("Documentation host: ")
    deploy_ccp_docs(doc_host=doc_host_input.strip())
