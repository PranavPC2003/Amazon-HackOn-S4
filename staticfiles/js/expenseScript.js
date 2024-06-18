const rangeInput1 = document.getElementById('rangeInput1');
const textInput1 = document.getElementById('textInput1');
const rangeInput2 = document.getElementById('rangeInput2');
const textInput2 = document.getElementById('textInput2');
const rangeInput3 = document.getElementById('rangeInput3');
const textInput3 = document.getElementById('textInput3');

let totalValue = 0;

function updateValue1(value) {
    rangeInput1.value = value;
    textInput1.value = value;
    totalValue -= rangeInput1.valueAsNumber - value;
    rangeInput1.valueAsNumber = value;
    updateTotal();
}

function updateValue2(value) {
    rangeInput2.value = value;
    textInput2.value = value;
    totalValue -= rangeInput2.valueAsNumber - value;
    rangeInput2.valueAsNumber = value;
    updateTotal();
}

function updateValue3(value) {
    rangeInput3.value = value;
    textInput3.value = value;
    totalValue -= rangeInput3.valueAsNumber - value;
    rangeInput3.valueAsNumber = value;
    updateTotal();
}

function updateTotal() {
    if (totalValue > 100) {
        totalValue = 100;
    }
    // rangeInput1.max = 100 - rangeInput2.valueAsNumber - rangeInput3.valueAsNumber;
    // rangeInput2.max = 100 - rangeInput1.valueAsNumber - rangeInput3.valueAsNumber;
    // rangeInput3.max = 100 - rangeInput1.valueAsNumber - rangeInput2.valueAsNumber;
}

rangeInput1.addEventListener('input', function() {
    let value = rangeInput1.value;
    if (value < 0) value = 0;
    if (value > 100 - rangeInput2.valueAsNumber - rangeInput3.valueAsNumber) value = 100 - rangeInput2.valueAsNumber - rangeInput3.valueAsNumber;
    updateValue1(value);
    totalValue += parseInt(value);
});

textInput1.addEventListener('input', function() {
    let value = textInput1.value;
    if (value < 0) value = 0;
    if (value > 100 - rangeInput2.valueAsNumber - rangeInput3.valueAsNumber) value = 100 - rangeInput2.valueAsNumber - rangeInput3.valueAsNumber;
    updateValue1(value);
    totalValue += parseInt(value);
});

rangeInput2.addEventListener('input', function() {
    let value = rangeInput2.value;
    if (value < 0) value = 0;
    if (value > 100 - rangeInput1.valueAsNumber - rangeInput3.valueAsNumber) value = 100 - rangeInput1.valueAsNumber - rangeInput3.valueAsNumber;
    updateValue2(value);
    totalValue += parseInt(value);
});

textInput2.addEventListener('input', function() {
    let value = textInput2.value;
    if (value < 0) value = 0;
    if (value > 100 - rangeInput1.valueAsNumber - rangeInput3.valueAsNumber) value = 100 - rangeInput1.valueAsNumber - rangeInput3.valueAsNumber;
    updateValue2(value);
    totalValue += parseInt(value);
});

rangeInput3.addEventListener('input', function() {
    let value = rangeInput3.value;
    if (value < 0) value = 0;
    if (value > 100 - rangeInput1.valueAsNumber - rangeInput2.valueAsNumber) value = 100 - rangeInput1.valueAsNumber - rangeInput2.valueAsNumber;
    updateValue3(value);
    totalValue += parseInt(value);
});

textInput3.addEventListener('input', function() {
    let value = textInput3.value;
    if (value < 0) value = 0;
    if (value > 100 - rangeInput1.valueAsNumber - rangeInput2.valueAsNumber) value = 100 - rangeInput1.valueAsNumber - rangeInput2.valueAsNumber;
    updateValue3(value);
    totalValue += parseInt(value);
});

updateValue1(rangeInput1.value);
updateValue2(rangeInput2.value);
updateValue3(rangeInput3.value);