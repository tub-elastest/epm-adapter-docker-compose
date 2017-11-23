node('docker'){
    stage "Container Prep"
        def mycontainer = docker.image('elastest/ci-docker-siblings:latest')
        mycontainer.pull() // make sure we have the latest available from Docker Hub

        mycontainer.inside("-u jenkins -v /var/run/docker.sock:/var/run/docker.sock:rw") {

            git 'https://github.com/mpauls/epm-client-docker-compose'

            stage "Build image - Package"
                echo ("Building docker image...")
                def myimage = docker.build("elastest/epm-docker-compose-driver")

            stage "Run image"
                echo "Run the image..."
                myimage.run()

            stage "Integration tests"
                echo ("Starting integration tests...")
                python -m tests.runtime_tests

            stage "Publish"
                echo ("Publishing as all tests succeeded...")
                //this is work arround as withDockerRegistry is not working properly
                withCredentials([[$class: 'UsernamePasswordMultiBinding', credentialsId: 'elastestci-dockerhub',
                              usernameVariable: 'USERNAME', passwordVariable: 'PASSWORD']]) {
                    sh 'docker login -u "$USERNAME" -p "$PASSWORD"'
                    myimage.push()
                }

        }
}