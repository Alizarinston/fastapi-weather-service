import inspect

import factory
from factory.builder import BuildStep, StepBuilder, parse_declarations


# https://github.com/FactoryBoy/factory_boy/issues/679#issuecomment-995289117
class AsyncFactory(factory.Factory):
    @classmethod
    async def _generate(cls, strategy, params):
        if cls._meta.abstract:
            raise factory.errors.FactoryError(
                'Cannot generate instances of abstract factory %(f)s; '
                'Ensure %(f)s.Meta.model is set and %(f)s.Meta.abstract '
                'is either not set or False.' % {'f': cls.__name__}
            )

        step = AsyncStepBuilder(cls._meta, params, strategy)
        return await step.build()

    @classmethod
    async def _create(cls, model_class, *args, **kwargs):
        for key, value in kwargs.items():
            if inspect.isawaitable(value):
                kwargs[key] = await value
        return await model_class.create(*args, **kwargs)

    @classmethod
    async def create_batch(cls, size, **kwargs):
        return [await cls.create(**kwargs) for _ in range(size)]


class AsyncStepBuilder(StepBuilder):
    async def build(self, parent_step=None, force_sequence=None):
        pre, post = parse_declarations(
            self.extras,
            base_pre=self.factory_meta.pre_declarations,
            base_post=self.factory_meta.post_declarations,
        )

        if force_sequence is not None:
            sequence = force_sequence

        elif self.force_init_sequence is not None:
            sequence = self.force_init_sequence
        else:
            sequence = self.factory_meta.next_sequence()

        step = BuildStep(
            builder=self,
            sequence=sequence,
            parent_step=parent_step,
        )
        step.resolve(pre)

        args, kwargs = self.factory_meta.prepare_arguments(step.attributes)

        instance = await self.factory_meta.instantiate(
            step=step,
            args=args,
            kwargs=kwargs,
        )

        postgeneration_results = {}

        for declaration_name in post.sorted():
            declaration = post[declaration_name]
            declaration_result = declaration.declaration.evaluate_post(
                instance=instance,
                step=step,
                overrides=declaration.context,
            )

            if inspect.isawaitable(declaration_result):
                declaration_result = await declaration_result

            postgeneration_results[declaration_name] = declaration_result

        self.factory_meta.use_postgeneration_results(
            instance=instance,
            step=step,
            results=postgeneration_results,
        )

        return instance
