node {
    docker.withRegistry('http://10.4.1.39:5000') {

        git url: "git@github.com:TAKEALOT/tal-locust.git", credentialsId: 'takealot-github-user'

        sh "git rev-parse --abbrev-ref HEAD > .git/branch-name"
        def branch = readFile('.git/branch-name').trim()

        stage "build"
        def app = docker.build "takealot/tal-locust"

        stage "publish"
        app.push "${branch}"
    }
}
