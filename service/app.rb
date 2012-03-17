require 'sinatra'

get '/' do
    puts 'request made'
    erb :index
end

$pages = {}

get '/:page' do
  @page = $pages[params[:page]] || []
  @xhr = request.xhr?
  erb :show, :layout => !@xhr
  
end

post '/:page' do
    $pages[params[:page]] ||= []
    $pages[params[:page]].push request.body.read
    "Success"
end
