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