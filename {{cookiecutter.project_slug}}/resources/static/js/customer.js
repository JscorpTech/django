
class Changer {
    constructor() {
        this.inputs = [];

        this.legal = [
            "bank_mfo",
            "bank_name",
            "bank_account",
            "name",
            "director_name",
            "responsible_person",
            "inn"
        ];

        this.physical = [
            "passport_series",
            "jshir",
            "first_name",
            "last_name",
        ]
        this.legal.concat(this.physical).forEach((item) => {
            this.inputs[item] = document.querySelector(`#id_${item}`).closest(".form-row");
        })
    }
    toggleDisplay(showItems, hideItems) {
        showItems.forEach(item => {
            this.inputs[item].style.display = "block";
        });
        hideItems.forEach(item => {
            this.inputs[item].style.display = "none";
        });
    };

    change(e) {
        if (e == "PHYSICAL") {
            this.toggleDisplay(this.physical, this.legal);
        } else if (e == "LEGAL") {
            this.toggleDisplay(this.legal, this.physical);
        }
    }
}

document.addEventListener("DOMContentLoaded", () => {
    let obj = new Changer();
    let select = document.querySelector("#id_person_type");
    select.addEventListener("change", (e) => obj.change(e.target.value));
    obj.change(select.value);
})