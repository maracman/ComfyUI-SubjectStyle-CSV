import pandas as pd
import os



def load_and_process_csv_file(csv_path):
    df = pd.read_csv(csv_path, dtype=str).fillna('')
    unique_styles = [col for col in df.columns if not col.startswith("_") and col != 'Unnamed: 0']
    styles = [f"{i+1}. {style}" for i, style in enumerate(unique_styles)]

    positive_prompts = []
    negative_prompts = []
    subjects = [f"{i+1}. {subject}" for i, subject in enumerate(df.iloc[:, 0])]

    for index, row in df.iterrows():
        subject_key = subjects[index]
        positive_dict = {"Subject": subject_key}
        negative_dict = {"Subject": subject_key}

        for style in unique_styles:
            style_key = f"{unique_styles.index(style)+1}. {style}"  # Use enumerated style
            positive_dict[style_key] = row[style]
            negative_col = f"_{style}" if f"_{style}" in df.columns else None
            negative_dict[style_key] = row[negative_col] if negative_col else "N/A"

        positive_prompts.append(positive_dict)
        negative_prompts.append(negative_dict)

    return styles, subjects, positive_prompts, negative_prompts

class CSVPromptProcessor:
    """
    Processes CSV data to extract prompts based on a selected row and column.
    Stores data from the selected row in an array of dictionaries with keys "name", "prompt", "negative_prompt".
    Populates a dropdown with the "name" entries from this dictionary.
    """

    def __init__(self):
            self.styles, self.subjects, self.positive_prompts, self.negative_prompts = self.load_and_process_csv()


    
    @classmethod
    def load_and_process_csv(cls):
        current_directory = os.path.dirname(os.path.realpath(__file__))
        csv_path = os.path.join(current_directory, 'csv_input', 'prompts_csv.csv')
        return load_and_process_csv_file(csv_path)
    
    @classmethod
    def INPUT_TYPES(cls):
        """Defines input types for the node, dynamically updated based on CSV content."""
        styles, subjects, _, _ = cls.load_and_process_csv()  # Ensure dynamic update
        return {
            "required": {
                "style": (styles, ),
                "subject": (subjects, ),
                "log_prompt": ("BOOLEAN", {"default": True, "label_on": "yes", "label_off": "no"}),
                "text_positive": ("STRING", {"default": "", "multiline": True}),
                "text_negative": ("STRING", {"default": "", "multiline": True}),
            },
        }


    FUNCTION = 'process_prompts'
    CATEGORY = 'CSV Processing'
    RETURN_TYPES = ('STRING', 'STRING')
    RETURN_NAMES = ('positive_prompt', 'negative_prompt')

    # Main functionality to append input text to the stored prompts
    def process_prompts(self, style, subject, text_positive, text_negative, log_prompt):
        # Find the matching style and subject in the stored prompts
        for prompt in self.positive_prompts:
            if prompt["Subject"] == subject and style in prompt:
                styled_positive_prompt = prompt[style] + " " + text_positive
                
        for prompt in self.negative_prompts:
            if prompt["Subject"] == subject and style in prompt:
                styled_negative_prompt = prompt[style] + " " + text_negative
                
        # Optional: Log the combined prompts if logging is enabled
        if log_prompt:
            print(f"Styled Positive Prompt: {styled_positive_prompt}")
            print(f"Styled Negative Prompt: {styled_negative_prompt}")
        
        return styled_positive_prompt, styled_negative_prompt



# Node Class and Display Name Mappings for integration
NODE_CLASS_MAPPINGS = {
    "CSVPromptProcessor": CSVPromptProcessor
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "CSVPromptProcessor": "CSV Prompt Processor"
}
