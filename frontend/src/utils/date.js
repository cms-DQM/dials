import { format } from 'date-fns'

const formatDate = (date, fmt) => {
  if (!date) {
    return ''
  }
  fmt = fmt || 'dd/MM/yyyy'
  return format(new Date(date), fmt)
}

export default formatDate
