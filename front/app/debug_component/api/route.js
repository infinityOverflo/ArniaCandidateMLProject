export async function GET() {
  return Response.json({ message: 'Hello Debug!' })
}

export async function POST(request) {
  const formData = await request.formData();
  if (!formData) {
    return Response.json({ error: 'No form data provided' }, { status: 400 });
  }
  return Response.json({ message: 'Form data received', data: Object.fromEntries(formData) }, { status: 200 });
}