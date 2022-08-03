
/* Typing Effect */
var j = 0;
var txt = 'Limited Time Offer ,Click Contact and Enjoyy!!!';
var speed = 50;


async function getUserDataFromAPI(event) {
  event.preventDefault();
  const id = document.getElementById("userId").value;
  const res = await fetch(`https://reqres.in/api/users/${id}`);
  user = await res.json();
  document.getElementById("userName").innerHTML = `<h3>Name: ${user?.data?.first_name} &nbsp Email: ${user?.data?.email}</h3>`;
  return false;
}

function typeWriter() {
    if (j < txt.length) {
        document.getElementById("demo").innerHTML += txt.charAt(j);
        j++;
        setTimeout(typeWriter, speed);
        }
      }


 /* Nav */
 
 const activePage = window.location.pathname;
 console.log(window.location.pathname); /*url שמזהה את העמוד*/

 const navLinks = document.querySelectorAll('nav a').forEach( link =>{
  if(link.href.includes(`${activePage}`)){
    link.classList.add('active');
  }
 });  




