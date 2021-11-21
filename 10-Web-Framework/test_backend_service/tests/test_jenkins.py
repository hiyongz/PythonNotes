from jenkinsapi.jenkins import Jenkins


def test_jenkins():
    jenkins = Jenkins(
        'http://stuq.ceshiren.com:8020/',
        username='seveniruby',
        password='11743b5e008e546ec1e404933d00b35a07'
    )


    jenkins['testcase'].invoke(
        securitytoken='11743b5e008e546ec1e404933d00b35a07',
        build_params={
            'testcases': '.'
        })

    print(jenkins['testcase'].get_last_completed_build().get_console())
