from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Div

from challenges.models import Solution
from challenges.tasks import validate_solution


class SolutionForm(forms.ModelForm):
    class Meta:
        model = Solution
        fields = ('solution', 'estimated_points')

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        self.challenge = kwargs.pop('challenge')

        super(SolutionForm, self).__init__(*args, **kwargs)

        self.fields['solution'].label = "Submit new solution file"
        self.fields['estimated_points'].label = "Perceived difficulty level in range of 1-100?"

        self.helper = FormHelper()
        self.helper.form_class = "form-horizontal"
        self.helper.label_class = "col-sm-6"
        self.helper.field_class = "col-sm-6"
        self.helper.layout = Layout(
            'solution',
            'estimated_points',
            Div(
                Div(
                    Submit('submit', 'Submit solution', css_class="btn btn-primary"),
                    css_class='col-sm-offset-6 col-sm-6',
                ),
                css_class='row',
            ),
        )

    def clean(self):
        cleaned_data = super(SolutionForm, self).clean()
        return cleaned_data

    def save(self, commit=True):
        solution = super(SolutionForm, self).save(commit=False)

        assert not solution.pk, "Solutions are not editable"

        solution.user = self.user
        solution.challenge = self.challenge
        solution.status = Solution.STATUS_SUBMITTED
        solution.solution_size = solution.solution.size

        if commit:
            solution.save()
            validate_solution.delay(solution.id)

        return solution
