from ospd_openvas.wrapper import OSPDopenvas, OSPD_PARAMS


class DummyWrapper(OSPDopenvas):
    def __init__(self, nvti, redis):

        self.VT = {
            '1.3.6.1.4.1.25623.1.0.100061': {
                'creation_time': '2009-03-19 11:22:36 +0100 (Thu, 19 Mar 2009)',
                'custom': {'category': '3',
                           'excluded_keys': 'Settings/disable_cgi_scanning',
                           'family': 'Product detection',
                           'filename': 'mantis_detect.nasl',
                           'required_ports': 'Services/www, 80',
                           'timeout': '0'},
                'modification_time': ('$Date: 2018-08-10 15:09:25 +0200 (Fri, '
                                      '10 Aug 2018) $'),
                'name': 'Mantis Detection',
                'qod_type': 'remote_banner',
                'insight': 'some insight',
                'severities': {
                    'severity_base_vector': 'AV:N/AC:L/Au:N/C:N/I:N/A:N',
                    'severity_type': 'cvss_base_v2'},
                'solution': 'some solution',
                'solution_type': 'WillNotFix',
                'impact': 'some impact',
                'summary': 'some summary',
                'vt_dependencies': [],
                'vt_params': {
                    'Data length : ': {
                        'default': '',
                        'description': 'Description',
                        'name': 'Data length : ',
                        'type': 'entry'},
                    'Do not randomize the  order  in  which ports are scanned': {
                        'default': 'no',
                        'description': 'Description',
                        'name': 'Do not randomize the  order  in  which ports are scanned',
                        'type': 'checkbox'},
                },
                'vt_refs': {
                    'bid': [''],
                    'cve': [''],
                    'xref': ['URL:http://www.mantisbt.org/']}}
            }

        oids = [['mantis_detect.nasl', '1.3.6.1.4.1.25623.1.0.100061']]
        nvti.get_oids.return_value = oids
        nvti.get_nvt_params.return_value = {
            'Data length : ': {
                'default': '',
                'description': 'Description',
                'name': 'Data length : ',
                'type': 'entry'
            },
            'Do not randomize the  order  in  which ports are scanned': {
                'default': 'no',
                'description': 'Description',
                'name': 'Do not randomize the  order  in  which ports are scanned',
                'type': 'checkbox'},
        }
        nvti.get_nvt_refs.return_value = {
            'bid': [''],
            'cve': [''],
            'xref': ['URL:http://www.mantisbt.org/']
        }
        nvti.get_nvt_metadata.return_value = {
            'category': '3',
            'creation_date': '2009-03-19 11:22:36 +0100 (Thu, 19 Mar 2009)',
            'cvss_base_vector': 'AV:N/AC:L/Au:N/C:N/I:N/A:N',
            'excluded_keys': 'Settings/disable_cgi_scanning',
            'family': 'Product detection',
            'filename': 'mantis_detect.nasl',
            'last_modification': (
                '$Date: 2018-08-10 15:09:25 +0200 (Fri, 10 Aug 2018) $'),
            'name': 'Mantis Detection',
            'qod_type': 'remote_banner',
            'required_ports': 'Services/www, 80',
            'solution': 'some solution',
            'solution_type': 'WillNotFix',
            'impact': 'some impact',
            'insight': 'some insight',
            'summary': ('some summary'),
            'timeout': '0'
        }

        self.openvas_db = redis
        self.nvti = nvti
        super(OSPDopenvas, self).__init__('cert', 'key', 'ca')
