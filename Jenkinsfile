pipeline {
    agent any
    stages {
        stage('echo stage') {
            steps {
	      echo "${ref}"   
	      echo "${created}"
	      echo "${deleted}"
            }
        }
    }
}

