let main = () => {
    let baseUrl = "http://127.0.0.1:8000/"
    let form = document.getElementById("signin-form")

    form.addEventListener("submit", (e) => {
        e.preventDefault()
        let formData = {
            "username": form.username.value,
            "password": form.password.value,
        }

        fetch(`${baseUrl}/api/users/token/`, {
            method: "POST",
            headers: {
                "Content-Type":"application/json",
            },
            body: JSON.stringify(formData)
        })
        .then(response => response.json())
        .then(data => {
            if(data.access) {
                localStorage.setItem("token", data.access)
                window.location = "file:///Users/ryan_toh/VSCodeProjects/frontend/projects-list.html"
            }
            else{
                alert("Username or Password incorrect")
            }

        })
    })


}

