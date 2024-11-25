---
permalink: /meet-the-team/
defaults:
# _pages
- scope:
  path: ""
  type: pages
  values:
  layout: single
---

<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
html {
  box-sizing: border-box;
}

*, *:before, *:after {
box-sizing: inherit;
}

.column {
float: left;
width: 50%;
margin-bottom: 16px;
padding: 0 8px;
}

@media screen and (max-width: 650px) {
.column {
width: 100%;
display: block;
}
}

.card {
box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2);
}

.container {
padding: 0 16px;
}

.container::after, .row::after {
content: "";
clear: both;
display: table;
}

.title {
color: grey;
}

.button {
border: none;
outline: 0;
display: inline-block;
padding: 8px;
color: white;
background-color: #000;
text-align: center;
cursor: pointer;
width: 100%;
}

.button:hover {
background-color: #555;
}
</style>
</head>
<body>

<h2>Meet Our Team :)</h2>
<br>

<div class="row">
  <div class="column">
    <div class="card">
      <img src="../assets/images/gberry.png" alt="George" style="width:100%">
      <div class="container">
        <h2>George Berry</h2>
        <p class="title">Developer</p>
        <p>I’m literally just a boy.</p>
        <p><button class="button"><a href="mailto:TODO@gmail.com" style="text-decoration:none !important; color:#FFFFFF;text-decoration:none;">Contact</a></button></p>
      </div>
    </div>
  </div>
  <div class="column">
    <div class="card">
      <img src="../assets/images/eneil.png" alt="Emily" style="width:100%">
      <div class="container">
        <h2>Emily Neil</h2>
        <p class="title">Developer</p>
        <p>I'm literally just a twink.</p>
        <p><button class="button"><a href="mailto:emilymianeil@gmail.com" style="text-decoration:none !important; color:#FFFFFF;text-decoration:none;">Contact</a></button></p>
      </div>
    </div>
  </div>
</div>

</body>
</html>
