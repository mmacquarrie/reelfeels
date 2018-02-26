$(document).ready(function() {
    var page = this.location.pathname;
    if (page != "/") page = page.substring(1);
    $('#main-nav .navbar-nav a.nav-link[href="' + page + '"]').parent().addClass('active');
});
