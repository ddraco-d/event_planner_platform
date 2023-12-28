// Можно добавить в helpers.js или использовать напрямую в компонентах


function userHasRole(requiredRole) {
    const userRole = this.$store.state.userRole;
    return userRole === requiredRole;
}