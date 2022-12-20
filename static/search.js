// const sanitizer1 = new Sanitizer(); // https://developer.mozilla.org/en-US/docs/Web/API/Element/setHTML

function highlightResult(query) {
// manipulate html output by adding spans and toggling css classes to query text
var texts = document.getElementsByClassName('resultText');  // the div to change
// directly using innerHTML creates a vector for CSS attacks by injecting HTML code, using DOMPurify to sanitize input.
// https://github.com/cure53/DOMPurify

Array.from(texts).forEach(element => {
    element.innerHTML = (DOMPurify.sanitize(element.innerHTML.replace(new RegExp('('+query+')','ig'), '<span class=highlight>$1</span>')));
});

// console.log(query);
}

const query = String(document.getElementsByClassName("resultCount")[0].textContent);
var highlightWord = 'NONE';
query !== "No results" ? highlightWord = query.match(new RegExp("\'(.*?)\'", "ig"))[0]: highlightWord = 'NONE';
highlightWord = highlightWord.substring(1, highlightWord.length-1);

console.log(highlightWord);
// window.onload = highlightResult(highlightWord);
// const queryInput = document.getElementById('query');
// queryInput.addEventListener('keyup',function(e){console.log(e)});
// const form = document.getElementById('searchForm');
// form.addEventListener('submit', function(e){console.log(e.target.childNodes[0]);})

// console.log(form.childNodes);

if (document.readyState == 'complete') {
    // highlightWord = queryInput.value;
    highlightResult(highlightWord);
} else {
    document.onreadystatechange = function () {
        if (document.readyState === "complete") {
            // highlightWord = queryInput.value;
            highlightResult(highlightWord);
        }
    }
}