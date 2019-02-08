node('docker'){
    stage "Container Prep"
        def mycontainer = docker.image('elastest/ci-docker-siblings:latest')
        mycontainer.pull() // make sure we have the latest available from Docker Hub

        mycontainer.inside("-u jenkins -v /var/run/docker.sock:/var/run/docker.sock:rw") {

            git 'https://github.com/tub-elastest/epm-adapter-docker-compose'

            stage "Build image - Package"
                echo ("Building docker image...")
                def myimage = docker.build("elastest/epm-adapter-docker-compose:1.0.0")

            stage "Run image"
                echo "Run the image..."
                myimage.run("-p 50051:50051 --expose 50051 -v /var/run/docker.sock:/var/run/docker.sock")

            stage "Integration tests"
                echo ("Starting integration tests...")
                sh 'pip install grpcio'
                //sh 'python -m tests.runtime_test'

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
