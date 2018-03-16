import lyte

secret_number = 4

def shift(c, howMuch= 1):
    return chr(ord(c) + howMuch)

def encoder(message):
    message=list(message)
    for i in range( len(message) ):
        message[i] = shift( message[i], howMuch=   secret_number )
    return ''.join(message)

def decoder(message):
    message=list(message)
    for i in range( len(message) ):
        message[i] = shift(message[i], howMuch=  - secret_number )
    return ''.join(message)

if __name__ == '__main__':
    message = 'this is a test'

    encoded_message = encoder(message)

    lyte.say(f' {message}  -->encoded-->  {encoded_message}  -->decoded--> {decoder(encoded_message)} ')

    lyte.webMe()
