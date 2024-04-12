const changeBadgeColor = (type, badge) => {
    if (type == 0) {
        badge.classList.remove('bg-danger');
        badge.classList.add('bg-success');
    } else if(type == 1) {
        badge.classList.remove('bg-success');
        badge.classList.add('bg-danger');
    }
}

export {changeBadgeColor}