// const sanitizer1 = new Sanitizer(); // https://developer.mozilla.org/en-US/docs/Web/API/Element/setHTML

function highlightResult(query) {
// manipulate html output by adding spans and toggling css classes to query text
var texts = document.getElementsByClassName('resultText');  // the div to change
// directly using innerHTML creates a vector for CSS attacks by injecting HTML code, using DOMPurify to sanitize input.
// https://github.com/cure53/DOMPurify
const pattern = /\<(.*?)\>/ig;
query = query.replaceAll(pattern, '\\w+');

Array.from(texts).forEach(element => {
    element.innerHTML = (DOMPurify.sanitize(element.innerHTML.replace(new RegExp('('+ query +')','ig'), '<span class="badge badge-info" >$1</span>')));
});
}

const query = String(document.getElementsByClassName("resultCount")[0].textContent);
var highlightWord = 'NONE';
query !== "No results" ? highlightWord = query.match(new RegExp("\'(.*?)\'", "ig"))[0]: highlightWord = 'NONE';
highlightWord = highlightWord.substring(1, highlightWord.length-1);

// console.log(highlightWord);

if (document.readyState == 'complete') {
    highlightResult(highlightWord);
} else {
    document.onreadystatechange = function () {
        if (document.readyState === "complete") {
            highlightResult(highlightWord);
        }
    }
}
const queryInput = document.getElementById('query');
const noun = document.getElementById('nounBtn');
const pron = document.getElementById('pronBtn');
const adj = document.getElementById('adjBtn');
const verb = document.getElementById('verbBtn');
const adv = document.getElementById('advBtn');
const adp = document.getElementById('adpBtn');
const prt = document.getElementById('prtBtn');
const det = document.getElementById('detBtn');
const conj = document.getElementById('conjBtn');
const num = document.getElementById('numBtn');

function addNoun(){
    queryInput.value += "<" + noun.textContent + "> ";
}
function addPron(){
    queryInput.value += "<" + pron.textContent + "> ";
}
function addAdj(){
    queryInput.value += "<" + adj.textContent + "> ";
}
function addVerb(){
    queryInput.value += "<" + verb.textContent + "> ";
}
function addAdv(){
    queryInput.value += "<" + adv.textContent + "> ";
}
function addAdp(){
    queryInput.value += "<" + adp.textContent + "> ";
}
function addPrt(){
    queryInput.value += "<" + prt.textContent + "> ";
}
function addDet(){
    queryInput.value += "<" + det.textContent + "> ";
}
function addConj(){
    queryInput.value += "<" + conj.textContent + "> ";
}
function addNum(){
    queryInput.value += "<" + num.textContent + "> ";
}