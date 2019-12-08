import random


def quotesCalculator(mood):
    """Calculate a random quote to display based on the user's mood"""
    # there is a panel of radio buttons from which the user selects one of a finite range of moods
    # for each possible mood, there is a list of quotes
    # the random module randomly generates a quote to be displayed
    if mood == 'unmotivated':
        quote = ['Success requires daily action', 'Do not limit your challenges, challenge your limits!',
                 'Push yourself, because no one else is going to do it for you.']
        return(random.choice(quote))
    elif mood == 'happy':
        quote = ['Happiness is a direction, not a place!', 'Choose Happy', 'The purpose of our lives is to be happy!']
        return(random.choice(quote))
    elif mood == 'sad':
        quote = ['Only when it is dark enough can you see the stars', 'Happiness comes in waves. It will find you again',
                 'You deserve to be happy. You deserve to live a life you are exited about. Do not let others make you forget that.']
        return(random.choice(quote))
    elif mood == 'mad':
        quote = ['I may look calm, but in my mind I have killed you three times',
                 'Anger is never without a reason, but seldom with a good one.', 'Channel your anger into productivity.']
        return(random.choice(quote))
    elif mood == 'stressed':
        quote = ['It is not the load you carry that breaks you down. It is the way you carry it.',
                 'Something it takes an overwhelming breakdown to have an undeniable breakthrough.',
                 'A year from now, everything you are stressing out about will not even matter.']
        return(random.choice(quote))
    elif mood == 'scared':
        quote = ['It is okay to be scared. Being scared means you are about to do something really, really brave.',
                 'There is no point of being scared of trying', 'Everything worth doing starts with being scared.']
        return(random.choice(quote))