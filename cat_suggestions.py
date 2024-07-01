tifrom cat.mad_hatter.decorators import hook

@hook (priority=1)
def before_cat_sends_message(message, cat):
    
    # Load settings
    settings = cat.mad_hatter.get_plugin().load_settings()
    num_suggestions = settings["number_of_suggestions"]

    if isinstance(num_suggestions, int) and num_suggestions > 0:

        # Prepare the prompt for the LLM to generate brief suggestions in the same language as the main content message
        prompt = f"""Per prima cosa, RIMUOVI TUTTI i suuggerimenti presenti nel messaggio principale. [<hr><div>Suggerimenti: ... </div>].
                    Poi, basato sul messaggio principale '{message[“content”]}’, genera {num_suggestions} suggerimenti unici per la prossima interazione. Ogni suggerimento dovrebbe offrire una prospettiva
                    o un’idea diversa correlata al contenuto principale. Assicurarsi che ogni suuggerimento sia concisa e nella stessa lingua del messaggio principale (massimo 6 parole e non utilizzare “, o .” alla fine).
                    """

        # Format the suggestions as clickable links in HTML
        suggestions_html = "After generating the suggestions, please format them as follows: " + \
                       "<hr><div> <b>Dritta: </b>" + ", ".join([f'<a href="javascript:void(0);" class="suggestion"><i>{{suggestion_{i+1}}}</i></a>' for i in range(num_suggestions)]) + "</div>"
        
        # Append the HTML-formatted suggestions to the prompt
        prompt += f"\n{suggestions_html}"

        # Request the LLM to generate suggestions based on the prompt
        suggestions = cat.llm(prompt, stream=True)

        #TO_DO: add suggestions in a new property
        # Append the generated suggestions to the message content
        message['content'] += suggestions

    return message
