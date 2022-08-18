// There are many ways to pick a DOM node; here we get the form itself and the email
// input box, as well as the span element into which we will place the error message.
const forms  = document.getElementsByTagName('form');
const inputs = document.getElementsByClassName('input-3');
const errorMessage = document.querySelector('div.error');

console.log(forms[0])

if(errorMessage.textContent != ''){
  if(errorMessage.textContent != 'Modifica eseguita'){errorMessage.className = 'error active';}
  else{errorMessage.className = 'error no_error';}
}

if(errorMessage){

  for (let i=0; i < inputs.length; i++){
    inputs[i].addEventListener('input', function (event) {
      // Each time the user types something, we check if the
      // form fields are valid.
      if (inputs[i].validity.valid) {
        errorMessage.textContent = ''; // Reset the content of the message
        errorMessage.className = 'error'; // Reset the visual state of the message
        if (!inputs[i].className.includes('log-in')){inputs[i].style.border ='2px solid #006840'}
      }
      else{
        // If there is still an error, show the correct error
        if (!inputs[i].className.includes('log-in')){inputs[i].style.border ='2px solid #900'}
      }
    });
  }
  
  for (let j=0; j<forms.length; j++){
    forms[j].addEventListener('submit', function (event) {
      // if the email field is valid, we let the form submit
      let i=0;
      let is_valid;
      do {
        is_valid = true;
        if(!inputs[i].validity.valid & inputs[i].form == forms[j]){
          is_valid = false;
          if(inputs[i].validity.valueMissing){
            errorMessage.textContent = `Compila tutti i campi`;
            console.log('ENTRATO D')
          } else if(inputs[i].validity.typeMismatch) {
            // If the field doesn't contain an email address, display the following error message.
            errorMessage.textContent = 'Devi inserire un indirizzo e-mail valido';
            console.log('ENTRATO A')
          } else if(inputs[i].validity.tooLong) {
            // If the data is too short, display the following error message.
            errorMessage.textContent = `${ inputs[i].name } deve essere lungo massimo ${ inputs[i].maxLength } caratteri`;
            console.log('ENTRATO B')
          } else if(inputs[i].validity.patternMismatch) {
            errorMessage.textContent = 'Inserisci una password valida'
            console.log('ENTRATO C')
          }
          errorMessage.className = 'error active';
          // Then we prevent the form from being sent by canceling the event
          event.preventDefault();
          i++;
        }
        i++;
      } while(i < inputs.length && is_valid);

    });
  }

}


