class Account {
    constructor(dict, parent) {
        this.id = Number(dict.id);
        this.name = dict.name;
        this.short_name = dict.short_name;

        this.html_parent = parent;
        this.html_object = document.createElement('option');
        this.html_object.setAttribute('value', this.id);
        this.html_object.innerText = this.short_name;

        this.html_parent.appendChild(this.html_object);
    }
}

class Category{
    constructor(dict, parent) {
        this.id = Number(dict.id);
        this.name = dict.name;
        this.is_subcategory = Boolean(dict.is_subcategory);
        this.is_income = Boolean(dict.is_income);
        this.parent_category_id = Number(dict.parent_category_id);

        this.html_parent = parent;
        this.html_object = document.createElement('option');
        this.html_object.setAttribute('value', this.id);
        this.html_object.innerText = this.name;

        this.html_parent.appendChild(this.html_object);
    }

    make_selectable() {
        this.html_object.classList.add('selectable')
    }

    make_unselectable() {
        this.html_object.classList.remove('selectable')
    }
}

const ACCOUNTS_LIST = [];
const CATEGORIES_LIST = [];
const SUBCATEGORIES_LIST = [];

(async () => {

    const expense_currency = document.getElementById('expense_account');
    const expense_category = document.getElementById('expense_category');
    const expense_subcategory = document.getElementById('expense_subcategory');

    document.getElementById('expense_datetime').value = new Date().toISOString().slice(0, 16);

    for (cur of await send_get_request('currency')) {
        ACCOUNTS_LIST.push(new Account(cur, expense_currency));
    }

    for (cur of await send_get_request('category')) {
        if (cur.parent_category_id) {
            SUBCATEGORIES_LIST.push(new Category(cur, expense_subcategory));
        } else {
            CATEGORIES_LIST.push(new Category(cur, expense_category));
        }
    }

    function on_select_category() {
        const category_id = Number(
            expense_category.options[expense_category.selectedIndex].getAttribute('value')
        );

        for (subcategory of SUBCATEGORIES_LIST) {
            if (subcategory.parent_category_id === category_id) {
                subcategory.make_selectable();
            } else {
                subcategory.make_unselectable();
            }
        }

        document.querySelector('#expense_subcategory option.selectable').selected = 1;
    }

    expense_category.addEventListener('change', on_select_category);
    on_select_category();

    document.getElementById('add_expense_form').addEventListener('submit', async function(event) {
        event.preventDefault();

        const form_data = {};

        (new FormData(this)).forEach(function(value, name) {
            form_data[name] = value;
        });

        log.debug('!?!?!?');

        log.debug(
            JSON.stringify(await send_post_request('transaction', form_data))
        );

    });


})();

// const DIALOG_ROUTE = 'dialog';
// const CHARACTER_ID = 1;
// let MERGE_MESSAGES_MODE = true;
// // what if message is selected but we still disable merge mode


// async function get_chain_of_messages(character_id) {
//     return await send_get_request(DIALOG_ROUTE, {'character_id':character_id});
// }


// class MessageField {
//     constructor(field_name, value, parent, html_block = 'span') {
//         this.html_object = document.createElement(html_block);
//         this.html_object.classList.add(`message_${field_name}`, 'message_field');
//         this.html_object.innerHTML = value;
//         this.field_name = field_name;
//         this.value = value;

//         parent.appendChild(this.html_object);
//     }
// }


// class MergeCheckbox {
//     constructor(message) {
//         // message: Message
//         this.message = message

//         this.html_object = document.createElement('div');
//         this.html_object.classList.add('merge_checkbox');
//         this.input_box = document.createElement('input');
//         this.input_box.setAttribute('type', 'checkbox');

//         this.html_object.appendChild(this.input_box);

//         this.input_box.addEventListener(
//             'change', async () => {await this._on_check.call(this)}
//         );

//         this.input_box.addEventListener(
//             'click', async () => {event.stopPropagation()}
//         );
//     }

//     is_checked() {
//         return this.input_box.checked;
//     }

//     check() {
//         this.input_box.checked = !this.input_box.checked;
//         this._on_check();
//     }

//     _on_check() {
//         if (this.input_box.checked) {
//             this.message.html_object.classList.add('selected_for_merge');
//         } else {
//             this.message.html_object.classList.remove('selected_for_merge');
//         }
//     }
// }


// class Message {

//     // html_object: html
//     // metadata: {html_object: html, fields: list[MessageField]}
//     // text: MessageField
//     // <field (from this.metadata.fields)>: MessageField

//     constructor(msg, parent) {
//         this.html_object = document.createElement('li');
//         this.html_object.classList.add('message');
//         this.content = document.createElement('div');
//         this.content.classList.add('content');

//         this.metadata = {
//             html_object: document.createElement('div'),
//             fields: []
//         };
//         this.metadata.html_object.classList.add('metadata')
//         this.html_object.appendChild(this.content);
//         this.content.appendChild(this.metadata.html_object);

//         for (const key in msg) {
//             if (msg.hasOwnProperty(key)) {
//                 this[key] = new MessageField(
//                     key, msg[key], key === 'text' ? this.content : this.metadata.html_object,
//                     key === 'text' ? 'div' : 'span',
//                 );
//                 if (key !== 'text') {
//                     this.metadata.fields.push(this[key]);
//                 }
//                 if (key === 'role') {
//                     if (msg[key] === 'user') {
//                         this.html_object.classList.add('user_message');
//                     } else {
//                         this.html_object.classList.add('assistant_message');
//                     }
//                 }
//             }
//         }

//         if (this.role.value != 'user') {
//             this.merge_checkbox = new MergeCheckbox(this);
//             this.html_object.appendChild(this.merge_checkbox.html_object);

//             this.html_object.addEventListener(
//                 'click', async () => {await this._on_click.call(this)}
//             );
//         }

//         parent.appendChild(this.html_object);
//     }

//     _on_click() {
//         if (this.merge_messages_mode()) {
//             this.merge_checkbox.check();
//         }
//     }

//     merge_messages_mode() {
//         return MERGE_MESSAGES_MODE;
//     }

//     delete() {
//         this.html_object.remove();
//     }
// }


// class ChainOfMessages {

//     // Represent list of messages.
//     // HTML analog is just plain ul.chain_of_messages list

//     // html_object: HTML
//     // character_id: int
//     // messages: list[Message]

//     constructor() {
//         this.character_id = CHARACTER_ID;  // TODO: SET

//         this.html_object = document.createElement('ul');
//         this.html_object.classList.add('chain_of_messages');

//         this.messages = [];
//     }

//     add_message(msg) {
//         this.messages.push(new Message(msg, this.html_object));
//     }

//     clear() {
//         for (const [index, msg] of Object.entries(this.messages)) {
//             msg.delete();
//             this.messages.splice(index, 1);
//         }
//     }

//     async synchronize_with_server() {
//         this.clear();

//         const chain_of_messages = await get_chain_of_messages(this.character_id);

//         for (let msg of chain_of_messages) {
//             this.add_message(msg);
//         }
//     }
// }


// class MessageInputBox {
//     constructor(chain_of_messages) {
//         // chain_of_messages: ChainOfMessages

//         this.character_id = CHARACTER_ID;  // TODO: SET
//         this.chain_of_messages = chain_of_messages;

//         this.html_object = document.createElement('div');
//         this.html_object.classList.add('message_input_box');

//         this.textarea = {
//             html_object:  document.createElement('textarea')
//         };
//         this.textarea.html_object.classList.add('message_textarea');
//         this.html_object.appendChild(this.textarea.html_object);

//         this.sending_button = {
//             html_object: document.createElement('button')
//         };
//         this.sending_button.html_object.classList.add('message_sending_button');
//         this.sending_button.html_object.innerText = 'Send'
//         this.html_object.appendChild(this.sending_button.html_object);

//         this.sending_button.html_object.addEventListener(
//             'click', async () => {await this.send_message.call(this)}
//         );
//     }

//     async send_message() {
//         const text = this.textarea.html_object.value;

//         if (text) {
//             JSON.stringify(await send_post_request(DIALOG_ROUTE, {
//                 'character_id': this.character_id, 'message': this.textarea.html_object.value}));

//             await this.chain_of_messages.synchronize_with_server();
//         }
//     }
// }

// class MainMenuSwitcher {
//     constructor(main_menu, mode, text_when_on, text_when_off, on_by_default=false, do_to_on=null, do_to_off=null) {
//         this.main_menu = main_menu;
//         this.mode = mode
//         this.text_when_on = text_when_on;
//         this.text_when_off = text_when_off;
//         this.on_by_default = on_by_default;
//         this.do_to_on = do_to_on;
//         this.do_to_off = do_to_off;
//         this.is_on = false;

//         this.html_object = document.createElement('li');
//         this.button = document.createElement('button');
//         this.html_object.classList.add('main_menu_option', `main_menu_option_${mode}`);

//         this.html_object.appendChild(this.button);

//         this.button.addEventListener(
//             'click', async () => {await this._on_click.call(this)}
//         );

//         if (on_by_default) {
//             this.enable();
//         } else {
//             this.disable();
//         }
//     }

//     _on_click() {
//         if (this.is_on) {
//             this.disable();
//         } else {
//             this.enable();
//         }
//     }

//     enable() {
//         this.html_object.classList.add('mode_on');
//         this.button.innerText = this.text_when_on;
//         this.is_on = true;

//         if (this.do_to_on) {
//             this.do_to_on();
//         }
//     }

//     disable() {
//         this.html_object.classList.remove('mode_on');
//         this.button.innerText = this.text_when_off;
//         this.is_on = false;

//         if (this.do_to_off) {
//             this.do_to_off();
//         }
//     }
// }

// class MainMenu {
//     constructor(main_menu_html, body_content) {
//         this.main_menu_html = main_menu_html;
//         this.body_content = body_content;

//         this.html_object = document.createElement('ul');
//         this.main_menu_html.appendChild(this.html_object);

//         this.merge_mod = new MainMenuSwitcher(
//             this, 'merge_mod', 'Merge mod is on', 'Merge mode is off', false,
//             () => {
//                 MERGE_MESSAGES_MODE = true;
//                 this.body_content.classList.add('merge_message_mod_on');
//             },
//             () => {
//                 MERGE_MESSAGES_MODE = false;
//                 this.body_content.classList.remove('merge_message_mod_on');
//             }
//         );

//         this.html_object.appendChild(this.merge_mod.html_object);
//     }
// }


// (async () => {

//     const BODY_CONTENT = document.getElementById('body_content');
//     const MAIN_MENU = new MainMenu(document.getElementById('main_menu'), BODY_CONTENT);

//     const CHAIN_OF_MESSAGES = new ChainOfMessages();
//     const MESSAGE_INPUT_BOX = new MessageInputBox(CHAIN_OF_MESSAGES);

//     BODY_CONTENT.appendChild(MESSAGE_INPUT_BOX.html_object);
//     BODY_CONTENT.appendChild(CHAIN_OF_MESSAGES.html_object);

//     await CHAIN_OF_MESSAGES.synchronize_with_server();

// })();
