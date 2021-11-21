from jenkinsapi.jenkins import Jenkins


def test_jenkins():
    jenkins = Jenkins(
        'http://192.168.30.8:8080/',
        username='admin',
        password='11d41f2fe7535bed739ce63c11f34a0216'
    )

    print(jenkins.keys())
    print(jenkins.version)
    print(jenkins.jobs.keys())
    print(jenkins.views.keys())
    jenkins.jobs.build("demo")
