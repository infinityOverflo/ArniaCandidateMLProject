export async function GET() {
  return Response.json({ message: 'Hello World' })
}

export async function POST(request) {
  const formData = await request.formData();
  const file = formData.get('file');

  if (!file) {
    return Response.json({ error: 'No file provided' }, { status: 400 });
  }

  // Process the file as needed
  // For example, you could save it to a specific location or perform some operations

  return Response.json({ message: 'File received successfully' });
}