
const compareForm = document.getElementById('compareForm').querySelector('form')
const submitBtn = compareForm.querySelector('input[type="submit"]')
const STRATEGY = ["desktop", "mobile"]

submitBtn.addEventListener('click', e=>{
    e.preventDefault()
    let isValid = true
    const url1 = compareForm.url_1
    const url2 = compareForm.url_2
    const  strategy= compareForm.strategy
    
    console.log(urlValidator(url1.value))
    if (!urlValidator(url1.value)) {
        isValid = false
        console.log(url1)
        url1.classList.add('is-invalid')
    }else{
        url1.classList.remove('is-invalid')
    }

    if (!urlValidator(url2.value)) {
        isValid = false
        url2.classList.add('is-invalid')
    }else{
        url2.classList.remove('is-invalid')
    }

    if(!STRATEGY.includes(strategy.value)){
        isValid = false
        strategy.classList.add('is-invalid')
    }else{
        strategy.classList.remove('is-invalid')
    }

    if (isValid) {
        compareForm.submit()
    }
})

function urlValidator(string) {
    let newUrl;
    try {
        newUrl = new URL(string)
    } catch (error) {
        console.log("ERROR: ", error)
        return false
    }

    return true
}
