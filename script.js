document.addEventListener('DOMContentLoaded', () => {
    const goalForm = document.getElementById('goal-form');
    const goalList = document.getElementById('goal-list');

    goalForm.addEventListener('submit', (e) => {
        e.preventDefault();

        const goalName = document.getElementById('goal-name').value;
        const goalTarget = document.getElementById('goal-target').value;

        if (goalName && goalTarget) {
            const listItem = document.createElement('li');
            listItem.innerHTML = `
                <span><strong>${goalName}</strong>: ${goalTarget} units</span>
                <button class="update">Update</button>
                <button class="delete">Delete</button>
            `;

            goalList.appendChild(listItem);

            document.getElementById('goal-name').value = '';
            document.getElementById('goal-target').value = '';

            listItem.querySelector('.delete').addEventListener('click', () => {
                listItem.remove();
            });

            listItem.querySelector('.update').addEventListener('click', () => {
                const newTarget = prompt('Update your target:', goalTarget);
                if (newTarget) {
                    listItem.querySelector('span').innerHTML = `<strong>${goalName}</strong>: ${newTarget} units`;
                }
            });
        }
    });
});
