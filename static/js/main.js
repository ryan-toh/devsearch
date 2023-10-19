// use queryselector to find the form
let searchForm = document.getElementById("searchForm")

// returns querySet of items
let pageLinks = document.getElementsByClassName("page-link")

// ensure search form exists
if(searchForm){
    // add event handler 
    for(let i=0; pageLinks.length > i; i++) {
        pageLinks[i].addEventListener("click", function (e) {
            e.preventDefault()

            // get 'data-page' attribute: "this" represents the pageLink
            let page = this.dataset.page
            console.log("PAGE: ", page)

            // add search input to form
            // use `` to add template literals with syntax ${<variableName>}
            searchForm.innerHTML += `<input value=${page} name="page" hidden/>`

            // submit form
            searchForm.submit()
        })

    }

}

let tags = document.getElementsByClassName("project--tag")
    
for(let i = 0; tags.length > i; i++){
    tags[i].addEventListener('click', (e) => {
        let tagId = e.target.dataset.tag
        let projectId = e.target.dataset.project

        fetch("http://127.0.0.1:8000/api/remove-tag/", {
            method: "DELETE",
            headers: {
                "Content-Type": "application/json"
            }, 
            body: JSON.stringify({'projectId': projectId, 'tagId': tagId})
        })
            .then(response => response.json())
            .then(data => {
                e.target.remove()
            })
    })
}