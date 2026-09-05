import { postForm } from './client'

export async function uploadImage(file: File) {
  const formData = new FormData()
  formData.append('file', file)
  const data = await postForm<{ image_url: string }>('/api/uploads/image', formData)
  return data.image_url
}
