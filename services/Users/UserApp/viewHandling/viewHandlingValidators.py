from UserApp.models import User  # Importing the custom User model 

"""
Username Validations:
it exists in the data
it is not empty
it is not already taken by another user
length is between 3 and 150 characters


Password Validations:
it exists in the data
it is not empty
it is at least 8 characters long
it contains at least one uppercase letter, one lowercase letter, one digit, and one special character
it does not contain the email address
it does not contain the first name or last name
it does not contain any characters that are not allowed in passwords (e.g., spaces, quotes, etc.)


first_name Validations:
it exists in the data
it is not empty


last_name Validations:
it exists in the data
it is not empty


email Validations:
it exists in the data
it is not empty
it is a valid email format
it is not already taken by another user


Date of Birth Validations:
it exists in the data
it is not empty
it is a valid date format (YYYY-MM-DD)
it is not a future date
it is not more than 100 years in the past


phone_number Validations:
it exists in the data
it is not empty
it is a valid phone number format (e.g., +1234567890)
it is not already taken by another user 


weight Validations:
it exists in the data
it is not empty
it is a valid decimal number
it is not less than 0
it is not more than 500 kg


height Validations:
it exists in the data
it is not empty
it is a valid positive integer
it is not less than 40 cm
it is not more than 300 cm


"""          
