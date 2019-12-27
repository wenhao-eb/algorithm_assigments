pipeline {
    agent any
    stages {
        stage('echo stage') {
            steps {
	      echo 'success'   
            }
        }
	stage('trigger test') {
	    when {
                  expression { return params.current_status == "closed" && params.merged == true }
              }
              steps {
                  echo 'trigger'
              }
	}
    }
}

