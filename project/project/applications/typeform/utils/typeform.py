import json
import logging
from typeform.models import TypeForm

logger = logging.getLogger(__name__)


def parse_typeform_answers(instance):
    def get_answer_name(form, answer_id):
        if not form:
            return answer_id
        if not form.questions.count():
            return answer_id
        question = form.questions.filter(question_id=answer_id).last()
        if not question:
            return answer_id
        return question.field_name

    content = json.loads(instance.content)
    form_id = content.get('form_id')
    form = None

    if TypeForm.objects.count():
        form = TypeForm.objects.filter(form_id=form_id).last()

    answers = {}
    for answer in content.get('answers'):
        answer_type = answer.get('type')
        if answer_type:
            answer_id = answer.get('field').get('id')
            answer_name = get_answer_name(form, answer_id)
            if answer_type == 'choice':
                answers[answer_name] = answer.get('choice').get('label')
            else:
                answers[answer_name] = answer.get(answer_type)

    instance.answers = json.dumps(answers, ensure_ascii=False, sort_keys=True)
    instance.form = form
    instance.save(update_fields=['answers', 'form'])
    logger.info('Typeform answers parsed')
    return form
