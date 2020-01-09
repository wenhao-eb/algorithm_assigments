#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import argparse
from subprocess import call, Popen, PIPE


def error_print(message):
    print('\033[91m%s\033[0m' % message)

def info_print(message):
    print('\033[92m%s\033[0m' % message)

try:
    import yaml
except:
    error_print('Please import yaml by running "sudo pip install pyyaml" first.')


class Deploy:
    TARGET_DIR='target'
    PROC_FILE_TEMPLATE='web: java -Dspring.profiles.active={env} -jar {jar}'

    def __init__(self, environment, release, dotenv_config_path=None):
        cur_dir = os.path.dirname(os.path.realpath(__file__))
        self.root_dir = os.path.join(cur_dir, '..')
        self.environment = environment


        if not self.validate_config_file():
            exit(1)

        jar_file = self.build_jar()
        if not jar_file or not os.path.isfile(os.path.join('%s/%s' %(self.root_dir, self.TARGET_DIR), jar_file)):
            error_print("Jar file build failed.")
            exit(1)

        self.package(jar_file)
        self.deploy_backend()

    def validate_config_file(self):
        config_path = os.path.join(self.root_dir, 'src/main/resources');
        config_file_name = 'application-%s.yml' % self.environment

        config_full_path = os.path.join(config_path, config_file_name)
        if not os.path.isfile(config_full_path):
            error_print("Please make sure you have a config file [%s] in {PROJECT_ROOT}/src/main/resources/" % config_file_name)
            return False

        with open(config_full_path, 'r') as stream:
            try:
                yaml.load(stream)
            except yaml.YAMLError as e:
                error_print(e)
                return False

        return True

    def build_jar(self):
        call(['rm', '-rf', self.TARGET_DIR])
        mvn_cmd = os.path.join(self.root_dir, 'mvnw')
        p = Popen([mvn_cmd, 'package', '-Dmaven.test.skip=true'], stdin=PIPE, stdout=sys.stdout, stderr=sys.stderr)
        p.communicate()
        error_code = p.returncode
        if error_code:
            return None

        p = Popen('ls %s/%s/*.jar | xargs -n 1 basename' %(self.root_dir, self.TARGET_DIR), shell=True, stdin=PIPE, stdout=PIPE)
        out, error = p.communicate()
        jar_name = self.byte_to_str(out).strip('\n')
        # gateway-0.0.1-SNAPSHOT.jar
        return jar_name

    def byte_to_str(self, b_str):
        if sys.version_info < (3, 0):
            return b_str.decode('utf-8').encode('utf-8')
        return str(b_str, 'utf-8')

    def package(self, jar_file):
        zip_dir = os.path.join(self.root_dir, self.TARGET_DIR, 'app')
        config_dir_in_zip = os.path.join(zip_dir, 'config')
        call(['mkdir', '-p', config_dir_in_zip])

        ebextensions_config_path = os.path.join(self.root_dir, '.ebextensions')

        # cp ebextensions directory
        call(['cp', '-r', ebextensions_config_path, zip_dir])

        config_path = os.path.join(self.root_dir, 'src/main/resources')
        config_file_name = 'application-%s.yml' % self.environment
        config_src_path = os.path.join(config_path, config_file_name)



        # cp config file
        call(['cp', config_src_path, config_dir_in_zip])

        # generate Procfile
        self.generate_procfile(jar_file)

        # cp jar file
        src_jar_file_path = os.path.join(self.root_dir, self.TARGET_DIR, jar_file)

        call(['cp', src_jar_file_path, zip_dir])

        # zip
        zip_file = 'app.zip'
        info_print('Package zip file...')
        p = Popen(['cd %s && zip -r %s ./' % (zip_dir, zip_file)], stdin=PIPE, stdout=sys.stdout, stderr=sys.stderr, shell=True)
        p.communicate()

    def generate_procfile(self, jar_file):
        proc_content = self.PROC_FILE_TEMPLATE.format(jar=jar_file, env=self.environment)
        zip_dir = os.path.join(self.root_dir, self.TARGET_DIR, 'app')
        proc_file_in_zip = os.path.join(zip_dir, 'Procfile')
        with open(proc_file_in_zip, 'w') as f:
            f.write(proc_content)

    def deploy_backend(self):
        info_print('Deploy backend to Elastic Beanstalk...')
        call(['eb', 'deploy'])

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Deploy to elasticbeanstalk')
    parser.add_argument("environment", nargs=1, choices=["dev", "qa", "staging", "prod"], help="Which environment you'd like to deploy to")
    parser.add_argument("-r", "--release-version", required=False, help="Release version number")
    args = parser.parse_args()
    environment = args.environment[0]
    release = args.release_version
    print(args)
    # Deploy(environment, release)

