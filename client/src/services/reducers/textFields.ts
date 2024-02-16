import { INPUT_FIELDS } from "./actions/types" 

enum InputUniqueIds {
    FirstName = 'firstName',
    LastName = 'lastName',
    Email = 'email',
    Password = 'password',
    ConfirmPassword = 'confirmPassword',
    Phone = 'phone',
    Address = 'address',
    City = 'city',
    State = 'state',
    Zip = 'zip',
    Country = 'country',
    CardName = 'cardName',
    CardNumber = 'cardNumber',
    Expiration = 'expiration',
    CVV = 'cvv',
    BillingZip = 'billingZip'
}

const initialState: { [key: string]: string } = {};

for (let item in InputUniqueIds) {
    if (isNaN(Number(item))) {
        const key = InputUniqueIds[item as keyof typeof InputUniqueIds];
        if (!initialState.hasOwnProperty(key)) {
            initialState[key] = '';
        }
    }
}


export const textFields = (state = initialState, action: any) => {    
    switch (action.type) {
        case INPUT_FIELDS:
            return {...state , ...action.payload};
        default:
            return state;
    }
}