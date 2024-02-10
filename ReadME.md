docker exec -i -t b1a21364e56d9c3d52f885f8753b7ebeca724dcf4088253f479e6e94deb8d620 console

s = box.schema.space.create('counter')

s:format({
{name = 'id', type = 'string'},
{name = 'userid', type = 'unsigned'},
{name = 'text', type = 'string'},
{name = 'status', type = 'string'},
})

s:create_index('primary', {
type = 'hash',
parts = {'id'}
})



box.space.counter:create_index('status', { parts = { { 'status' } }, unique = false })

box.space['counter']:insert{ 1, 1, 'TextPost', 'Publish'}

box.space['counter']:select()
box.space['counter']:count()

box.space['counter'].index.status:select {'Publish'} // Все опубликованные
box.space['counter'].index.status:count {'Publish'} // Количество опубликованн