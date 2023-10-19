let main = () => {
    let projectsUrl = "http://127.0.0.1:8000/api/projects"
    let baseUrl = "http://127.0.0.1:8000"

    let loginButton = document.getElementById("login-btn")
    let logoutButton = document.getElementById("logout-btn")

    let token = localStorage.getItem("token")

    if (token) {
        loginButton.remove()
    } else {
        logoutButton.remove()
    }

    logoutButton.addEventListener('click', (e) => {
        e.preventDefault()
        localStorage.removeItem('token')
        window.location = "file:///Users/ryan_toh/VSCodeProjects/frontend/login.html"
    })

    let getProjects = () => {
        // sends a GET request
        fetch(projectsUrl)
        // .then waits until the previous line is executed
        .then(response => response.json())
        .then(data => {
            buildProjects(data)
        })
    }

    let buildProjects = (projects) => {
        let projectsWrapper = document.getElementById("projects-wrapper")
        projectsWrapper.innerHTML = ''
        for (let i = 0; projects.length > i; i = i+1){
            let project = projects[i]
            console.log(project)
            let projectCard = `
                <div class="project--card">
                    <img src=${baseUrl}${project.featured_image}>
                    <div>
                        <div class="card--header">
                            <h3>
                                ${project.title}
                            </h3>
                            <strong class="vote--option" data-vote="up" data-project="${project.id}">&#43;</strong>
                            <strong class="vote--option" data-vote="down" data-project="${project.id}">&#8722;</strong>
                        </div>
                        <i>${project.vote_ratio}% Positive feedback</i>
                        <p>${project.description.substring(0, 150)}</p>
                    </div>
                </div>
            `
            projectsWrapper.innerHTML += projectCard
        }

        // add event listener
        addVoteEvents()

    }

    let addVoteEvents = () => {
        let voteButton = document.getElementsByClassName("vote--option")
        
        for (let i=0; voteButton.length > i; i++) {
            voteButton[i].addEventListener("click", (e) => {
                let token = localStorage.getItem("token")
                let vote = e.target.dataset.vote
                let project = e.target.dataset.project
                console.log(token)
                
                fetch(`${baseUrl}/api/projects/vote/${project}/`, {
                    method:"POST",
                    headers: {
                        "Content-Type": "application/json",
                        Authorization: `Bearer ${token}`

                    },
                    body: JSON.stringify({"value": vote, "body": ""})
                })
                .then(response => response.json())
                .then(data => {
                    console.log("Success", data)
                    getProjects()
                })

            })
        }

    }

    getProjects()
}
